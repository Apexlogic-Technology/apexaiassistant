# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_work_orders(parameters, user):
	"""
	Get work orders
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		if parameters.get("production_item"):
			filters["production_item"] = parameters["production_item"]
		
		if parameters.get("from_date"):
			filters["planned_start_date"] = [">=", parameters["from_date"]]
		
		# Get work orders
		work_orders = frappe.get_all(
			"Work Order",
			filters=filters,
			fields=[
				"name", "production_item", "item_name", "qty", "produced_qty",
				"status", "planned_start_date", "planned_end_date", "actual_start_date"
			],
			order_by="planned_start_date desc",
			limit=100
		)
		
		return {
			"success": True,
			"message": f"Found {len(work_orders)} work orders",
			"data": {
				"work_orders": work_orders,
				"total_count": len(work_orders)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Work Orders Error")
		return {
			"success": False,
			"message": f"Error retrieving work orders: {str(e)}",
			"error": str(e)
		}

def get_bom_summary(parameters, user):
	"""
	Get Bill of Materials summary
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("item"):
			filters["item"] = parameters["item"]
		
		if parameters.get("is_active"):
			filters["is_active"] = 1
		
		if parameters.get("is_default"):
			filters["is_default"] = 1
		
		# Get BOMs
		boms = frappe.get_all(
			"BOM",
			filters=filters,
			fields=[
				"name", "item", "item_name", "quantity", "is_active",
				"is_default", "total_cost", "creation"
			],
			order_by="creation desc",
			limit=100
		)
		
		return {
			"success": True,
			"message": f"Found {len(boms)} BOMs",
			"data": {
				"boms": boms,
				"total_count": len(boms)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get BOM Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving BOMs: {str(e)}",
			"error": str(e)
		}
