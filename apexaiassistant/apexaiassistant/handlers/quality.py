# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_quality_inspections(parameters, user):
	"""
	Get quality inspections
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		if parameters.get("inspection_type"):
			filters["inspection_type"] = parameters["inspection_type"]
		
		if parameters.get("item_code"):
			filters["item_code"] = parameters["item_code"]
		
		# Get inspections
		inspections = frappe.get_all(
			"Quality Inspection",
			filters=filters,
			fields=[
				"name", "item_code", "item_name", "inspection_type", "status",
				"inspected_by", "report_date", "sample_size", "reference_type", "reference_name"
			],
			order_by="report_date desc",
			limit=100
		)
		
		# Calculate summary
		total_inspections = len(inspections)
		status_breakdown = {}
		
		for inspection in inspections:
			status = inspection.get("status", "Unknown")
			status_breakdown[status] = status_breakdown.get(status, 0) + 1
		
		return {
			"success": True,
			"message": f"Found {total_inspections} quality inspections",
			"data": {
				"inspections": inspections,
				"total_count": total_inspections,
				"status_breakdown": status_breakdown
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Quality Inspections Error")
		return {
			"success": False,
			"message": f"Error retrieving quality inspections: {str(e)}",
			"error": str(e)
		}

def get_quality_goals(parameters, user):
	"""
	Get quality goals
	"""
	try:
		filters = {}
		
		# Get quality goals
		goals = frappe.get_all(
			"Quality Goal",
			filters=filters,
			fields=[
				"name", "goal", "target", "frequency", "revision"
			],
			order_by="creation desc",
			limit=50
		)
		
		return {
			"success": True,
			"message": f"Found {len(goals)} quality goals",
			"data": {
				"goals": goals,
				"total_count": len(goals)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Quality Goals Error")
		return {
			"success": False,
			"message": f"Error retrieving quality goals: {str(e)}",
			"error": str(e)
		}
