# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json
import os
import pandas as pd

def analyze_file(parameters, user):
	"""
	Analyzes uploaded CSV/Excel files using Pandas
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		file_url = parameters.get("file_url")
		analysis_type = parameters.get("analysis_type", "summary")
		
		if not file_url:
			return {"success": False, "error": "file_url is required"}
		
		# Resolve file path
		site_path = frappe.get_site_path()
		if file_url.startswith("/private/files/"):
			file_path = os.path.join(site_path, "private", "files", file_url.replace("/private/files/", ""))
		elif file_url.startswith("/files/"):
			file_path = os.path.join(site_path, "public", "files", file_url.replace("/files/", ""))
		else:
			return {"success": False, "error": "Invalid file_url format"}
			
		if not os.path.exists(file_path):
			return {"success": False, "error": f"File not found on server at {file_path}"}
			
		# Load dataframe
		try:
			if file_path.endswith(".csv"):
				df = pd.read_csv(file_path)
			elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
				df = pd.read_excel(file_path)
			else:
				return {"success": False, "error": "Only CSV and Excel files are supported"}
		except Exception as e:
			return {"success": False, "error": f"Could not read file data: {str(e)}"}
			
		# Perform requested analysis
		if analysis_type == "summary":
			result = {
				"row_count": len(df),
				"column_count": len(df.columns),
				"columns": list(df.columns),
				"data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
				"null_counts": df.isnull().sum().to_dict()
			}
			
		elif analysis_type == "statistics":
			# Only get stats for numeric columns to avoid errors
			numeric_df = df.select_dtypes(include=['number'])
			if numeric_df.empty:
				return {"success": False, "error": "No numeric columns found for statistical analysis"}
				
			desc = numeric_df.describe().to_dict()
			
			# Add median manually since describe doesn't always include it depending on pandas version
			median = numeric_df.median().to_dict()
			for col in desc:
				desc[col]["median"] = median.get(col)
				
			result = {"statistics": desc}
			
		elif analysis_type == "correlations":
			numeric_df = df.select_dtypes(include=['number'])
			if numeric_df.empty or len(numeric_df.columns) < 2:
				return {"success": False, "error": "Need at least 2 numeric columns for correlation analysis"}
				
			# Calculate correlation matrix, replace NaN with 0 for JSON serialization
			corr = numeric_df.corr().fillna(0).to_dict()
			result = {"correlations": corr}
			
		else:
			return {"success": False, "error": f"Unsupported analysis_type '{analysis_type}'"}
			
		return {
			"success": True,
			"data": result
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "File Analysis Error")
		return {"success": False, "error": str(e)}
