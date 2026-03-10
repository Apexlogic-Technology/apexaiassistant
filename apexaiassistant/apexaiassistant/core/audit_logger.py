# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe

class AuditLogger:
	"""
	Logs all actions performed by ApexAiAssistant for audit trail
	"""
	
	@staticmethod
	def log_action(user, action_name, action_category, status, query=None, result=None, error_message=None, session_id=None):
		"""
		Create an audit log entry
		"""
		try:
			audit_log = frappe.get_doc({
				"doctype": "ApexAiAssistant Audit Log",
				"user": user,
				"action_name": action_name,
				"action_category": action_category,
				"status": status,
				"timestamp": frappe.utils.now(),
				"session_id": session_id,
				"query": query,
				"result": result,
				"error_message": error_message
			})
			audit_log.insert(ignore_permissions=True)
			frappe.db.commit()
			
			return audit_log.name
			
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Audit Logger Error")
			# Don't fail the main operation if audit logging fails
			return None
	
	@staticmethod
	def get_user_activity(user, limit=50):
		"""
		Get recent activity for a user
		"""
		return frappe.get_all(
			"ApexAiAssistant Audit Log",
			filters={"user": user},
			fields=["name", "action_name", "action_category", "status", "timestamp"],
			order_by="timestamp desc",
			limit=limit
		)
	
	@staticmethod
	def get_action_history(action_name, limit=50):
		"""
		Get history of a specific action
		"""
		return frappe.get_all(
			"ApexAiAssistant Audit Log",
			filters={"action_name": action_name},
			fields=["name", "user", "status", "timestamp"],
			order_by="timestamp desc",
			limit=limit
		)
