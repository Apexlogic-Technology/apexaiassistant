# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.utils import add_days, getdate, nowdate
import datetime

def generate_chart_data(parameters, user):
	"""
	Generates interactive visualizations from ERPNext data
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		chart_type = parameters.get("chart_type", "bar")
		query_type = parameters.get("query_type")
		
		# Allow read-only access to sales analysis or similar
		if query_type == "sales_by_customer":
			# Mocking simple fetch for the AI to present
			data = frappe.db.sql('''
				SELECT customer, sum(base_grand_total) as total 
				FROM `tabSales Invoice` 
				WHERE docstatus = 1 
				GROUP BY customer ORDER BY total DESC LIMIT 10
			''', as_dict=True)
			
			return {
				"success": True,
				"data": {
					"chart_type": chart_type,
					"labels": [d.customer for d in data],
					"datasets": [{"name": "Revenue", "values": [d.total for d in data]}],
					"title": "Top Customers by Revenue"
				}
			}
			
		elif query_type == "revenue_trends":
			data = frappe.db.sql('''
				SELECT MONTHNAME(posting_date) as month, sum(base_grand_total) as total 
				FROM `tabSales Invoice` 
				WHERE docstatus = 1 AND YEAR(posting_date) = YEAR(CURDATE())
				GROUP BY MONTH(posting_date) ORDER BY MONTH(posting_date)
			''', as_dict=True)
			
			return {
				"success": True,
				"data": {
					"chart_type": chart_type if chart_type != "bar" else "line",
					"labels": [d.month for d in data],
					"datasets": [{"name": "Monthly Revenue", "values": [d.total for d in data]}],
					"title": "Revenue Trends (Current Year)"
				}
			}
			
		return {"success": False, "error": f"Unsupported query_type '{query_type}'"}

	except Exception as e:
		return {"success": False, "error": str(e)}


def forecast_sales(parameters, user):
	"""
	Sales Forecasting using simple heuristics / trends.
	Enterprise version would use pandas/sklearn for linear regression,
	but we handle safe DB querying and simple calculations.
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		forecast_period_days = parameters.get("forecast_period_days", 30)
		
		# Get daily sales for last 90 days to determine moving average based forecast
		data = frappe.db.sql(f'''
			SELECT posting_date, sum(base_grand_total) as total 
			FROM `tabSales Invoice` 
			WHERE docstatus = 1 AND posting_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
			GROUP BY posting_date ORDER BY posting_date
		''', as_dict=True)
		
		if not data:
			return {"success": True, "data": {"message": "Not enough historical data to generate forecast."}}
			
		total_revenue = sum(d.total for d in data)
		avg_daily = total_revenue / 90.0
		
		forecast_value = avg_daily * forecast_period_days
		
		return {
			"success": True,
			"data": {
				"forecast_period": f"{forecast_period_days} days",
				"historical_avg_daily": avg_daily,
				"predicted_revenue": forecast_value,
				"confidence": "Medium (Based on 90-day moving average)"
			}
		}

	except Exception as e:
		return {"success": False, "error": str(e)}

def segment_customers_rfm(parameters, user):
	"""
	Customer Segmentation using RFM (Recency, Frequency, Monetary)
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		data = frappe.db.sql('''
			SELECT 
				customer, 
				DATEDIFF(CURDATE(), MAX(posting_date)) as recency,
				COUNT(name) as frequency,
				SUM(base_grand_total) as monetary
			FROM `tabSales Invoice`
			WHERE docstatus = 1
			GROUP BY customer
		''', as_dict=True)
		
		if not data:
			return {"success": True, "data": {"message": "No sales data found to perform RFM segmentation."}}
			
		# Simple bucketing algorithm
		# Sort for Monetary
		data.sort(key=lambda x: x.monetary, reverse=True)
		
		segments = {
			"Champions": [],
			"Loyal Customers": [],
			"At Risk": [],
			"Lost": []
		}
		
		for row in data:
			if row.recency <= 30 and row.frequency >= 5:
				segments["Champions"].append(row.customer)
			elif row.recency <= 90 and row.frequency >= 2:
				segments["Loyal Customers"].append(row.customer)
			elif row.recency > 180 and row.frequency > 1:
				segments["At Risk"].append(row.customer)
			elif row.recency > 365:
				segments["Lost"].append(row.customer)
				
		return {
			"success": True,
			"data": segments
		}
		
	except Exception as e:
		return {"success": False, "error": str(e)}

def predict_churn(parameters, user):
	"""
	Churn Prediction based on declining activity
	"""
	try:
		data = frappe.db.sql('''
			SELECT 
				customer, 
				MAX(posting_date) as last_order_date,
				DATEDIFF(CURDATE(), MAX(posting_date)) as days_since_last_order
			FROM `tabSales Invoice`
			WHERE docstatus = 1
			GROUP BY customer
			HAVING days_since_last_order > 90 AND days_since_last_order <= 365
			ORDER BY days_since_last_order DESC
			LIMIT 50
		''', as_dict=True)
		
		return {
			"success": True,
			"data": {
				"at_risk_customers": data,
				"message": f"Found {len(data)} customers at risk of churning (no orders in 90-365 days)."
			}
		}
	except Exception as e:
		return {"success": False, "error": str(e)}
