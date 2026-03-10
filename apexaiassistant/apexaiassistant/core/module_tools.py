# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

class ModuleIntelligenceTools:
	"""
	Tools for deep module-specific analytical intelligence mapping
	to HR, Manufacturing, Finance, and Projects.
	"""
	
	@staticmethod
	def get_financial_aging_analysis(user):
		"""Get AR/AP Aging Analysis"""
		try:
			# Mocking structural data for Accounts Receivable
			query = """
				SELECT 
					party as customer,
					SUM(CASE WHEN delay <= 30 THEN outstanding_amount ELSE 0 END) as '0_30_days',
					SUM(CASE WHEN delay > 30 AND delay <= 60 THEN outstanding_amount ELSE 0 END) as '31_60_days',
					SUM(CASE WHEN delay > 60 AND delay <= 90 THEN outstanding_amount ELSE 0 END) as '61_90_days',
					SUM(CASE WHEN delay > 90 THEN outstanding_amount ELSE 0 END) as '90_plus_days',
					SUM(outstanding_amount) as total_outstanding
				FROM (
					SELECT 
						customer as party, 
						outstanding_amount, 
						DATEDIFF(CURDATE(), due_date) as delay
					FROM `tabSales Invoice`
					WHERE docstatus = 1 AND outstanding_amount > 0 AND due_date < CURDATE()
				) as aging_data
				GROUP BY party
				ORDER BY total_outstanding DESC
				LIMIT 20
			"""
			data = frappe.db.sql(query, as_dict=True)
			
			if not data:
				return {"message": "No outstanding receivables found.", "success": True}
				
			return {
				"message": "Accounts Receivable Aging Analysis",
				"data": {"aging_analysis": data},
				"type": "table",
				"success": True
			}
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "ApexAiAssistant Financial Aging Error")
			return {"message": f"Error calculating aging: {str(e)}", "success": False}

	@staticmethod
	def get_manufacturing_efficiency(user):
		"""Get Manufacturing Production Efficiency"""
		try:
			query = """
				SELECT 
					production_item,
					COUNT(name) as total_orders,
					SUM(qty) as planned_qty,
					SUM(produced_qty) as produced_qty,
					ROUND((SUM(produced_qty) / SUM(qty)) * 100, 2) as efficiency_percentage
				FROM `tabWork Order`
				WHERE docstatus = 1 AND status IN ('Completed', 'In Process')
				GROUP BY production_item
				ORDER BY efficiency_percentage DESC
				LIMIT 20
			"""
			data = frappe.db.sql(query, as_dict=True)
			
			if not data:
				return {"message": "No active manufacturing work orders found.", "success": True}
				
			return {
				"message": "Manufacturing Production Efficiency",
				"data": {"efficiency": data},
				"type": "table",
				"success": True
			}
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "ApexAiAssistant Manufacturing Error")
			return {"message": f"Error calculating manufacturing efficiency: {str(e)}", "success": False}

	@staticmethod
	def get_hr_leave_balances(user):
		"""Get Employee Leave Balances"""
		try:
			query = """
				SELECT 
					employee,
					employee_name,
					leave_type,
					total_leaves_allocated,
					leaves_taken,
					(total_leaves_allocated - leaves_taken) as remaining_balance
				FROM `tabLeave Allocation`
				WHERE docstatus = 1 AND to_date >= CURDATE()
				ORDER BY remaining_balance ASC
				LIMIT 30
			"""
			data = frappe.db.sql(query, as_dict=True)
			
			if not data:
				return {"message": "No active leave allocations found.", "success": True}
				
			return {
				"message": "Employee Leave Balances",
				"data": {"leave_balances": data},
				"type": "table",
				"success": True
			}
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "ApexAiAssistant HR Leave Error")
			return {"message": f"Error fetching leave balances: {str(e)}", "success": False}
