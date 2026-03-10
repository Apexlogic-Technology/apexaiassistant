# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_projects_summary(parameters, user):
	"""
	Get projects summary
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		if parameters.get("project_type"):
			filters["project_type"] = parameters["project_type"]
		
		# Get projects
		projects = frappe.get_all(
			"Project",
			filters=filters,
			fields=[
				"name", "project_name", "status", "project_type", 
				"expected_start_date", "expected_end_date", "percent_complete",
				"customer", "total_costing_amount", "total_billing_amount"
			],
			order_by="creation desc",
			limit=100
		)
		
		# Calculate summary
		total_projects = len(projects)
		total_cost = sum(p.get("total_costing_amount", 0) for p in projects)
		total_billing = sum(p.get("total_billing_amount", 0) for p in projects)
		avg_completion = sum(p.get("percent_complete", 0) for p in projects) / total_projects if total_projects > 0 else 0
		
		return {
			"success": True,
			"message": f"Found {total_projects} projects",
			"data": {
				"projects": projects,
				"total_count": total_projects,
				"total_cost": total_cost,
				"total_billing": total_billing,
				"average_completion": avg_completion
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Projects Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving projects: {str(e)}",
			"error": str(e)
		}

def get_tasks_summary(parameters, user):
	"""
	Get tasks summary
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("project"):
			filters["project"] = parameters["project"]
		
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		if parameters.get("assigned_to"):
			filters["_assign"] = ["like", f"%{parameters['assigned_to']}%"]
		
		# Get tasks
		tasks = frappe.get_all(
			"Task",
			filters=filters,
			fields=[
				"name", "subject", "status", "priority", "project",
				"exp_start_date", "exp_end_date", "progress", "description"
			],
			order_by="creation desc",
			limit=100
		)
		
		return {
			"success": True,
			"message": f"Found {len(tasks)} tasks",
			"data": {
				"tasks": tasks,
				"total_count": len(tasks)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Tasks Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving tasks: {str(e)}",
			"error": str(e)
		}
