# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_employee_list(parameters, user):
	"""
	Get employee list
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		if parameters.get("department"):
			filters["department"] = parameters["department"]
		
		if parameters.get("designation"):
			filters["designation"] = parameters["designation"]
		
		# Get employees
		employees = frappe.get_all(
			"Employee",
			filters=filters,
			fields=[
				"name", "employee_name", "department", "designation",
				"date_of_joining", "status", "company", "cell_number", "personal_email"
			],
			order_by="employee_name",
			limit=100
		)
		
		return {
			"success": True,
			"message": f"Found {len(employees)} employees",
			"data": {
				"employees": employees,
				"total_count": len(employees)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Employee List Error")
		return {
			"success": False,
			"message": f"Error retrieving employee list: {str(e)}",
			"error": str(e)
		}

def approve_leave(parameters, user):
	"""
	Approve a leave application
	"""
	try:
		# Validate required parameters
		if not parameters.get("leave_application"):
			return {
				"success": False,
				"message": "Leave Application name is required",
				"error": "Missing leave_application"
			}
		
		# Get leave application
		leave_app = frappe.get_doc("Leave Application", parameters["leave_application"])
		
		# Check if user has permission to approve
		if not frappe.has_permission("Leave Application", "write", leave_app.name, user=user):
			return {
				"success": False,
				"message": "You don't have permission to approve this leave application",
				"error": "Permission denied"
			}
		
		# Check current status
		if leave_app.status == "Approved":
			return {
				"success": False,
				"message": "This leave application is already approved",
				"error": "Already approved"
			}
		
		# Approve the leave
		leave_app.status = "Approved"
		leave_app.save()
		
		return {
			"success": True,
			"message": f"Leave application {leave_app.name} has been approved",
			"data": {
				"leave_application": leave_app.name,
				"employee": leave_app.employee_name,
				"from_date": leave_app.from_date,
				"to_date": leave_app.to_date,
				"leave_type": leave_app.leave_type
			},
			"type": "action",
			"category": "APPROVE"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Approve Leave Error")
		return {
			"success": False,
			"message": f"Error approving leave: {str(e)}",
			"error": str(e)
		}
