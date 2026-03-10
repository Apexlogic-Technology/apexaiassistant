# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_account_balances(parameters, user):
	"""
	Get account balances
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("account"):
			filters["name"] = parameters["account"]
		
		if parameters.get("account_type"):
			filters["account_type"] = parameters["account_type"]
		
		if parameters.get("root_type"):
			filters["root_type"] = parameters["root_type"]
		
		# Get accounts
		accounts = frappe.get_all(
			"Account",
			filters=filters,
			fields=[
				"name", "account_name", "account_type", "root_type",
				"is_group", "parent_account", "account_currency"
			],
			limit=100
		)
		
		# Get GL entries to calculate balances
		for account in accounts:
			if not account.get("is_group"):
				# Get balance from GL Entry
				balance = frappe.db.sql("""
					SELECT 
						SUM(debit) - SUM(credit) as balance
					FROM `tabGL Entry`
					WHERE account = %s
					AND is_cancelled = 0
				""", account["name"], as_dict=True)
				
				account["balance"] = balance[0]["balance"] if balance else 0
		
		return {
			"success": True,
			"message": f"Found {len(accounts)} accounts",
			"data": {
				"accounts": accounts,
				"total_count": len(accounts)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Account Balances Error")
		return {
			"success": False,
			"message": f"Error retrieving account balances: {str(e)}",
			"error": str(e)
		}

def create_journal_entry_draft(parameters, user):
	"""
	Create a draft journal entry
	"""
	try:
		# Validate required parameters
		if not parameters.get("accounts"):
			return {
				"success": False,
				"message": "Accounts are required to create a journal entry",
				"error": "Missing accounts"
			}
		
		# Create journal entry
		je = frappe.get_doc({
			"doctype": "Journal Entry",
			"posting_date": parameters.get("posting_date", frappe.utils.today()),
			"voucher_type": parameters.get("voucher_type", "Journal Entry"),
			"company": parameters.get("company") or frappe.defaults.get_user_default("Company"),
			"accounts": parameters["accounts"],
			"user_remark": parameters.get("user_remark")
		})
		
		# Don't save yet, just return the draft
		return {
			"success": True,
			"message": "Journal entry draft created. Please review and save.",
			"data": {
				"doctype": "Journal Entry",
				"doc": je.as_dict()
			},
			"type": "draft",
			"category": "DRAFT"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Create Journal Entry Draft Error")
		return {
			"success": False,
			"message": f"Error creating journal entry draft: {str(e)}",
			"error": str(e)
		}
