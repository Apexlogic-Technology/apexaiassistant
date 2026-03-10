# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json
import re

def execute_sql_query(parameters, user):
	"""
	Executes AI-generated SQL query safely (Read-only)
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		query = parameters.get("query")
		
		if not query:
			return {"success": False, "error": "Query string is required"}
		
		# Validation for dangerous SQL keywords
		dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "REPLACE", "GRANT", "REVOKE", "INTO"]
		
		upper_query = query.upper()
		for kw in dangerous_keywords:
			# Look for whole word matches to avoid false positives inside strings or column names
			if re.search(r'\b' + kw + r'\b', upper_query):
				return {
					"success": False,
					"error": f"Security violation: Action blocked. Query contains prohibited keyword '{kw}'."
				}
				
		# Only allow SELECT queries
		if not upper_query.strip().startswith("SELECT"):
			return {
				"success": False,
				"error": "Security violation: Only SELECT queries are permitted."
			}
			
		# Check permissions loosely at system manager level, or by restricting doctypes,
		# but for simplicity we rely on System Manager only having this action.
		if "System Manager" not in frappe.get_roles(user):
			return {"success": False, "error": "Only System Managers can execute raw SQL."}

		# Limit rows for safety
		if "LIMIT" not in upper_query:
			query += " LIMIT 100"

		results = frappe.db.sql(query, as_dict=True)
		
		return {
			"success": True,
			"data": {
				"query": query,
				"results": results,
				"count": len(results)
			}
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "NL SQL Error")
		return {"success": False, "error": f"Database error: {str(e)}"}
