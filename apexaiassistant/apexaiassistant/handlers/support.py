# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_issues_summary(parameters, user):
	"""
	Get support issues summary
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		if parameters.get("priority"):
			filters["priority"] = parameters["priority"]
		
		if parameters.get("customer"):
			filters["customer"] = parameters["customer"]
		
		# Get issues
		issues = frappe.get_all(
			"Issue",
			filters=filters,
			fields=[
				"name", "subject", "customer", "status", "priority",
				"issue_type", "opening_date", "resolution_date", "raised_by"
			],
			order_by="opening_date desc",
			limit=100
		)
		
		# Calculate summary
		total_issues = len(issues)
		status_breakdown = {}
		priority_breakdown = {}
		
		for issue in issues:
			status = issue.get("status", "Unknown")
			priority = issue.get("priority", "Unknown")
			status_breakdown[status] = status_breakdown.get(status, 0) + 1
			priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
		
		return {
			"success": True,
			"message": f"Found {total_issues} support issues",
			"data": {
				"issues": issues,
				"total_count": total_issues,
				"status_breakdown": status_breakdown,
				"priority_breakdown": priority_breakdown
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Issues Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving issues: {str(e)}",
			"error": str(e)
		}

def get_service_level_summary(parameters, user):
	"""
	Get service level agreement summary
	"""
	try:
		filters = {}
		
		# Get SLA data
		sla_compliance = frappe.db.sql("""
			SELECT 
				i.priority,
				COUNT(*) as total,
				SUM(CASE WHEN i.resolution_date IS NOT NULL 
					AND i.resolution_date <= i.response_by THEN 1 ELSE 0 END) as met_sla,
				AVG(TIMESTAMPDIFF(HOUR, i.opening_date, i.resolution_date)) as avg_resolution_hours
			FROM `tabIssue` i
			WHERE i.status != 'Open'
			GROUP BY i.priority
		""", as_dict=True)
		
		return {
			"success": True,
			"message": "SLA compliance summary",
			"data": {
				"sla_compliance": sla_compliance
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Service Level Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving SLA data: {str(e)}",
			"error": str(e)
		}
