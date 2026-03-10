# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_stock_summary(parameters, user):
	"""
	Get stock levels and summary
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("item_code"):
			filters["item_code"] = parameters["item_code"]
		
		if parameters.get("warehouse"):
			filters["warehouse"] = parameters["warehouse"]
		
		if parameters.get("item_group"):
			filters["item_group"] = parameters["item_group"]
		
		# Get stock balances
		stock_balances = frappe.get_all(
			"Bin",
			filters=filters,
			fields=[
				"item_code", "warehouse", "actual_qty", "reserved_qty",
				"ordered_qty", "projected_qty", "valuation_rate"
			],
			limit=100
		)
		
		# Get item details
		for balance in stock_balances:
			item = frappe.get_cached_value(
				"Item",
				balance["item_code"],
				["item_name", "stock_uom", "item_group"],
				as_dict=True
			)
			balance.update(item)
		
		# Calculate summary
		total_items = len(stock_balances)
		total_value = sum(
			balance.get("actual_qty", 0) * balance.get("valuation_rate", 0)
			for balance in stock_balances
		)
		
		return {
			"success": True,
			"message": f"Found stock data for {total_items} items",
			"data": {
				"stock_balances": stock_balances,
				"total_items": total_items,
				"total_value": total_value
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Stock Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving stock data: {str(e)}",
			"error": str(e)
		}
