# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_purchase_orders(parameters, user):
	"""
	Get purchase orders
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("from_date"):
			filters["transaction_date"] = [">=", parameters["from_date"]]
		if parameters.get("to_date"):
			if "transaction_date" in filters:
				filters["transaction_date"] = ["between", [parameters["from_date"], parameters["to_date"]]]
			else:
				filters["transaction_date"] = ["<=", parameters["to_date"]]
		
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		if parameters.get("supplier"):
			filters["supplier"] = parameters["supplier"]
		
		# Get purchase orders
		purchase_orders = frappe.get_all(
			"Purchase Order",
			filters=filters,
			fields=[
				"name", "supplier", "transaction_date", "schedule_date",
				"grand_total", "status", "per_received", "per_billed"
			],
			order_by="transaction_date desc",
			limit=100
		)
		
		# Calculate summary
		total_amount = sum(po.get("grand_total", 0) for po in purchase_orders)
		
		return {
			"success": True,
			"message": f"Found {len(purchase_orders)} purchase orders",
			"data": {
				"purchase_orders": purchase_orders,
				"total_count": len(purchase_orders),
				"total_amount": total_amount
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Purchase Orders Error")
		return {
			"success": False,
			"message": f"Error retrieving purchase orders: {str(e)}",
			"error": str(e)
		}
