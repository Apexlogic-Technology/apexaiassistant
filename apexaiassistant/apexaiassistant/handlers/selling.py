# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days, nowdate

def get_sales_orders(parameters, user):
	"""
	Get sales orders with detailed analytics
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
		
		if parameters.get("customer"):
			filters["customer"] = parameters["customer"]
		
		# Get sales orders
		sales_orders = frappe.get_all(
			"Sales Order",
			filters=filters,
			fields=[
				"name", "customer", "customer_name", "transaction_date", "delivery_date",
				"grand_total", "status", "per_delivered", "per_billed", "currency", "order_type"
			],
			order_by="transaction_date desc",
			limit=100
		)
		
		# Calculate summary
		total_amount = sum(so.get("grand_total", 0) for so in sales_orders)
		status_breakdown = {}
		
		for so in sales_orders:
			status = so.get("status", "Unknown")
			status_breakdown[status] = status_breakdown.get(status, 0) + 1
		
		return {
			"success": True,
			"message": f"Found {len(sales_orders)} sales orders",
			"data": {
				"sales_orders": sales_orders,
				"total_count": len(sales_orders),
				"total_amount": total_amount,
				"status_breakdown": status_breakdown
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Sales Orders Error")
		return {
			"success": False,
			"message": f"Error retrieving sales orders: {str(e)}",
			"error": str(e)
		}

def get_pending_sales_orders(parameters, user):
	"""
	Get pending/outstanding sales orders
	"""
	try:
		# Get sales orders that are not fully delivered or billed
		pending_orders = frappe.db.sql("""
			SELECT 
				name, customer, customer_name, transaction_date, delivery_date,
				grand_total, status, per_delivered, per_billed,
				(grand_total - advance_paid) as outstanding_amount
			FROM `tabSales Order`
			WHERE docstatus = 1
			AND status NOT IN ('Completed', 'Closed', 'Cancelled')
			AND (per_delivered < 100 OR per_billed < 100)
			ORDER BY delivery_date ASC
			LIMIT 100
		""", as_dict=True)
		
		total_outstanding = sum(o.get("outstanding_amount", 0) for o in pending_orders)
		
		# Overdue orders
		overdue = [o for o in pending_orders if getdate(o.delivery_date) < getdate()]
		
		return {
			"success": True,
			"message": f"Found {len(pending_orders)} pending sales orders",
			"data": {
				"pending_orders": pending_orders,
				"total_count": len(pending_orders),
				"overdue_count": len(overdue),
				"total_outstanding": total_outstanding
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Pending Sales Orders Error")
		return {
			"success": False,
			"message": f"Error retrieving pending orders: {str(e)}",
			"error": str(e)
		}

def get_quotations_summary(parameters, user):
	"""
	Get quotations summary with conversion tracking
	"""
	try:
		filters = {}
		
		if parameters.get("from_date"):
			filters["transaction_date"] = [">=", parameters["from_date"]]
		if parameters.get("to_date"):
			if "transaction_date" in filters:
				filters["transaction_date"] = ["between", [parameters["from_date"], parameters["to_date"]]]
			else:
				filters["transaction_date"] = ["<=", parameters["to_date"]]
		
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		# Get quotations
		quotations = frappe.get_all(
			"Quotation",
			filters=filters,
			fields=[
				"name", "party_name", "transaction_date", "valid_till",
				"grand_total", "status", "order_type", "quotation_to"
			],
			order_by="transaction_date desc",
			limit=100
		)
		
		# Calculate conversion
		total_quotations = len(quotations)
		converted = len([q for q in quotations if q.status == "Ordered"])
		conversion_rate = (converted / total_quotations * 100) if total_quotations > 0 else 0
		
		total_value = sum(q.get("grand_total", 0) for q in quotations)
		
		return {
			"success": True,
			"message": f"Found {total_quotations} quotations with {conversion_rate:.2f}% conversion rate",
			"data": {
				"quotations": quotations,
				"total_count": total_quotations,
				"converted_count": converted,
				"conversion_rate": conversion_rate,
				"total_value": total_value
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Quotations Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving quotations: {str(e)}",
			"error": str(e)
		}

def get_sales_analytics(parameters, user):
	"""
	Get comprehensive sales analytics
	"""
	try:
		from_date = parameters.get("from_date", add_days(nowdate(), -30))
		to_date = parameters.get("to_date", nowdate())
		
		# Sales by customer
		sales_by_customer = frappe.db.sql("""
			SELECT 
				customer,
				customer_name,
				COUNT(*) as order_count,
				SUM(grand_total) as total_sales
			FROM `tabSales Order`
			WHERE docstatus = 1
			AND transaction_date BETWEEN %s AND %s
			GROUP BY customer
			ORDER BY total_sales DESC
			LIMIT 10
		""", (from_date, to_date), as_dict=True)
		
		# Sales by item group
		sales_by_item = frappe.db.sql("""
			SELECT 
				i.item_group,
				SUM(soi.amount) as total_amount,
				SUM(soi.qty) as total_qty
			FROM `tabSales Order Item` soi
			INNER JOIN `tabSales Order` so ON soi.parent = so.name
			INNER JOIN `tabItem` i ON soi.item_code = i.name
			WHERE so.docstatus = 1
			AND so.transaction_date BETWEEN %s AND %s
			GROUP BY i.item_group
			ORDER BY total_amount DESC
			LIMIT 10
		""", (from_date, to_date), as_dict=True)
		
		# Monthly trend
		monthly_trend = frappe.db.sql("""
			SELECT 
				DATE_FORMAT(transaction_date, '%%Y-%%m') as month,
				COUNT(*) as order_count,
				SUM(grand_total) as total_sales
			FROM `tabSales Order`
			WHERE docstatus = 1
			AND transaction_date BETWEEN %s AND %s
			GROUP BY month
			ORDER BY month
		""", (from_date, to_date), as_dict=True)
		
		return {
			"success": True,
			"message": "Sales analytics generated",
			"data": {
				"top_customers": sales_by_customer,
				"sales_by_item_group": sales_by_item,
				"monthly_trend": monthly_trend,
				"period": f"{from_date} to {to_date}"
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Sales Analytics Error")
		return {
			"success": False,
			"message": f"Error generating analytics: {str(e)}",
			"error": str(e)
		}

def create_sales_order_draft(parameters, user):
	"""
	Create a draft sales order
	"""
	try:
		# Validate required parameters
		if not parameters.get("customer"):
			return {
				"success": False,
				"message": "Customer is required to create a sales order",
				"error": "Missing customer"
			}
		
		if not parameters.get("items"):
			return {
				"success": False,
				"message": "Items are required to create a sales order",
				"error": "Missing items"
			}
		
		# Create sales order
		so = frappe.get_doc({
			"doctype": "Sales Order",
			"customer": parameters["customer"],
			"transaction_date": parameters.get("transaction_date", frappe.utils.today()),
			"delivery_date": parameters.get("delivery_date"),
			"items": parameters["items"]
		})
		
		# Don't save yet, just return the draft
		return {
			"success": True,
			"message": "Sales order draft created. Please review and save.",
			"data": {
				"doctype": "Sales Order",
				"doc": so.as_dict()
			},
			"type": "draft",
			"category": "DRAFT"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Create Sales Order Draft Error")
		return {
			"success": False,
			"message": f"Error creating sales order draft: {str(e)}",
			"error": str(e)
		}
