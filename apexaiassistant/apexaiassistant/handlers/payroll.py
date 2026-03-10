# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute_payroll(parameters, user):
	"""
	Execute payroll for a period
	This is a critical operation and should be done with care
	"""
	try:
		# Validate required parameters
		if not parameters.get("payroll_entry"):
			return {
				"success": False,
				"message": "Payroll Entry name is required",
				"error": "Missing payroll_entry"
			}
		
		# Get payroll entry
		payroll = frappe.get_doc("Payroll Entry", parameters["payroll_entry"])
		
		# Check if user has permission
		if not frappe.has_permission("Payroll Entry", "write", payroll.name, user=user):
			return {
				"success": False,
				"message": "You don't have permission to execute this payroll",
				"error": "Permission denied"
			}
		
		# Check if already submitted
		if payroll.docstatus == 1:
			return {
				"success": False,
				"message": "This payroll entry is already submitted",
				"error": "Already submitted"
			}
		
		# Create salary slips if not already created
		if not payroll.salary_slips_created:
			payroll.fill_employee_details()
			payroll.create_salary_slips()
		
		# Get summary
		total_employees = len(payroll.employees)
		
		return {
			"success": True,
			"message": f"Payroll executed for {total_employees} employees. Please review and submit the payroll entry.",
			"data": {
				"payroll_entry": payroll.name,
				"total_employees": total_employees,
				"payroll_period": f"{payroll.start_date} to {payroll.end_date}",
				"company": payroll.company
			},
			"type": "action",
			"category": "EXECUTE_PAYROLL"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Execute Payroll Error")
		return {
			"success": False,
			"message": f"Error executing payroll: {str(e)}",
			"error": str(e)
		}
