# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_maintenance_schedule(parameters, user):
	"""
	Get maintenance schedule
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("customer"):
			filters["customer"] = parameters["customer"]
		
		# Get maintenance schedules
		schedules = frappe.get_all(
			"Maintenance Schedule",
			filters=filters,
			fields=[
				"name", "customer", "transaction_date", "status"
			],
			order_by="transaction_date desc",
			limit=100
		)
		
		return {
			"success": True,
			"message": f"Found {len(schedules)} maintenance schedules",
			"data": {
				"schedules": schedules,
				"total_count": len(schedules)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Maintenance Schedule Error")
		return {
			"success": False,
			"message": f"Error retrieving maintenance schedules: {str(e)}",
			"error": str(e)
		}

def get_maintenance_visits(parameters, user):
	"""
	Get maintenance visits
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("status"):
			filters["completion_status"] = parameters["status"]
		
		if parameters.get("customer"):
			filters["customer"] = parameters["customer"]
		
		# Get maintenance visits
		visits = frappe.get_all(
			"Maintenance Visit",
			filters=filters,
			fields=[
				"name", "customer", "customer_name", "mntc_date", 
				"completion_status", "maintenance_type"
			],
			order_by="mntc_date desc",
			limit=100
		)
		
		return {
			"success": True,
			"message": f"Found {len(visits)} maintenance visits",
			"data": {
				"visits": visits,
				"total_count": len(visits)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Maintenance Visits Error")
		return {
			"success": False,
			"message": f"Error retrieving maintenance visits: {str(e)}",
			"error": str(e)
		}
