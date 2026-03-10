# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json
from frappe import _
from apexaiassistant.apexaiassistant.core.orchestrator import AIOrchestrator
from apexaiassistant.apexaiassistant.core.audit_logger import AuditLogger

@frappe.whitelist()
def send_message(message, session_id=None):
	"""
	Send a message to the AI assistant
	"""
	try:
		user = frappe.session.user
		
		# Create or get session
		if not session_id:
			session = frappe.get_doc({
				"doctype": "AI Conversation",
				"user": user,
				"title": message[:50] + "..." if len(message) > 50 else message,
				"messages_json": "[]"
			})
			session.insert()
			session_id = session.name
		else:
			session = frappe.get_doc("AI Conversation", session_id)
		
		messages = json.loads(session.messages_json or "[]")
		
		# Add user message to session
		messages.append({
			"role": "user",
			"content": message
		})
		
		session.db_set("messages_json", json.dumps(messages))
		
		# Process with AI Orchestrator
		orchestrator = AIOrchestrator()
		response = orchestrator.process_message(message, session_id, user)
		
		# Add assistant response to session
		messages.append({
			"role": "assistant",
			"content": response.get("message", ""),
			"action_taken": response.get("action_taken"),
			"action_result": response.get("action_result")
		})
		
		session.db_set("messages_json", json.dumps(messages))
		
		return {
			"success": True,
			"session_id": session_id,
			"response": response
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "ApexAiAssistant Chat Error")
		return {
			"success": False,
			"error": str(e)
		}

@frappe.whitelist()
def get_sessions():
	"""
	Get all chat sessions for the current user
	"""
	try:
		user = frappe.session.user
		sessions = frappe.get_all(
			"AI Conversation",
			filters={"user": user},
			fields=["name", "title", "modified as last_message_at"],
			order_by="modified desc"
		)
		return {
			"success": True,
			"sessions": sessions
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "ApexAiAssistant Get Sessions Error")
		return {
			"success": False,
			"error": str(e)
		}

@frappe.whitelist()
def get_session_messages(session_id):
	"""
	Get all messages from a chat session
	"""
	try:
		session = frappe.get_doc("AI Conversation", session_id)
		
		# Check if user has access to this session
		if session.user != frappe.session.user and not frappe.has_permission("AI Conversation", "read", session):
			frappe.throw(_("You don't have permission to view this session"))
		
		messages = json.loads(session.messages_json or "[]")
		
		return {
			"success": True,
			"messages": messages
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "ApexAiAssistant Get Messages Error")
		return {
			"success": False,
			"error": str(e)
		}

@frappe.whitelist()
def confirm_action(session_id, action_name, parameters):
	"""
	Confirm and execute a pending action
	"""
	try:
		user = frappe.session.user
		orchestrator = AIOrchestrator()
		
		# Parse parameters if it's a string
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
		
		result = orchestrator.execute_action(action_name, parameters, user)
		
		# Log the action
		AuditLogger.log_action(
			user=user,
			action_name=action_name,
			action_category=result.get("category"),
			status="Success" if result.get("success") else "Failed",
			query=json.dumps(parameters),
			result=json.dumps(result.get("data")),
			error_message=result.get("error"),
			session_id=session_id
		)
		
		return result
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "ApexAiAssistant Confirm Action Error")
		return {
			"success": False,
			"error": str(e)
		}
