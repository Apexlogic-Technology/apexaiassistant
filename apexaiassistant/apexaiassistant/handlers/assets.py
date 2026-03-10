# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_assets_summary(parameters, user):
	"""
	Get assets summary
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("asset_category"):
			filters["asset_category"] = parameters["asset_category"]
		
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		if parameters.get("location"):
			filters["location"] = parameters["location"]
		
		# Get assets
		assets = frappe.get_all(
			"Asset",
			filters=filters,
			fields=[
				"name", "asset_name", "asset_category", "status", "location",
				"purchase_date", "gross_purchase_amount", "available_for_use_date",
				"custodian"
			],
			order_by="purchase_date desc",
			limit=100
		)
		
		# Calculate summary
		total_assets = len(assets)
		total_value = sum(a.get("gross_purchase_amount", 0) for a in assets)
		status_breakdown = {}
		
		for asset in assets:
			status = asset.get("status", "Unknown")
			status_breakdown[status] = status_breakdown.get(status, 0) + 1
		
		return {
			"success": True,
			"message": f"Found {total_assets} assets",
			"data": {
				"assets": assets,
				"total_count": total_assets,
				"total_value": total_value,
				"status_breakdown": status_breakdown
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Assets Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving assets: {str(e)}",
			"error": str(e)
		}

def get_asset_maintenance_schedule(parameters, user):
	"""
	Get asset maintenance schedule
	"""
	try:
		filters = {}
		
		if parameters.get("asset"):
			filters["asset_name"] = parameters["asset"]
		
		# Get maintenance schedule
		schedules = frappe.get_all(
			"Asset Maintenance Task",
			filters=filters,
			fields=[
				"name", "asset_name", "maintenance_type", "next_due_date",
				"maintenance_status", "periodicity", "assign_to"
			],
			order_by="next_due_date",
			limit=100
		)
		
		return {
			"success": True,
			"message": f"Found {len(schedules)} maintenance tasks",
			"data": {
				"maintenance_tasks": schedules,
				"total_count": len(schedules)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Asset Maintenance Schedule Error")
		return {
			"success": False,
			"message": f"Error retrieving maintenance schedule: {str(e)}",
			"error": str(e)
		}
