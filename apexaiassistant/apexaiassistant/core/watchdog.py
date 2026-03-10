# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json
from apexaiassistant.apexaiassistant.core.orchestrator import AIOrchestrator

def run_watchdogs():
	"""
	Main trigger function fired by Frappe Scheduler (hourly).
	Triggers independent AI watchdog agents to scan the database.
	"""
	frappe.enqueue("apexaiassistant.apexaiassistant.core.watchdog._check_stale_leads", queue="long")
	frappe.enqueue("apexaiassistant.apexaiassistant.core.watchdog._check_inventory_anomalies", queue="long")

def _check_stale_leads():
	"""
	AI Agent that scans for Leads with no interaction in the last 7 days.
	Drafts an analysis and alerts the Sales Manager.
	"""
	try:
		# Note: DATE_SUB syntax varies. In Frappe (MariaDB), it's standard.
		stale_leads = frappe.db.sql("""
			SELECT name, lead_name, company_name, status, creation 
			FROM `tabLead` 
			WHERE status IN ('Lead', 'Open') 
			AND modified < DATE_SUB(NOW(), INTERVAL 7 DAY) 
			LIMIT 15
		""", as_dict=True)
		
		if not stale_leads:
			return

		settings = frappe.get_single("ApexAiAssistant Settings")
		if not settings.openai_api_key:
			return

		prompt = f"""You are the proactive AI Watchdog for ERPNext.
Please review the following list of stagnant Sales Leads that haven't had any CRM activity in over 7 days.
Write a concise, professional 3-sentence notification for the Sales Manager urging them to follow up.
Do not use formatting, just raw text.

Leads: {json.dumps(stale_leads)}"""

		# Use litellm directly to save overhead
		import litellm
		model = settings.ai_model or "gpt-4o"
		if settings.ai_provider == "Anthropic": model = "anthropic/" + model
		
		response = litellm.completion(
			model=model,
			messages=[{"role": "user", "content": prompt}],
			api_key=settings.get_password("api_key"),
			api_base=settings.api_url if settings.api_url else None
		)
		
		alert_text = response.choices[0].message.content
		
		# Send Frappe System Notification
		_send_notification("AI Watchdog: Stale Leads Detected", alert_text)
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "AI Watchdog Leads Error")

def _check_inventory_anomalies():
	"""
	AI Agent that scans for Inventory items dropping unexpectedly faster than average.
	"""
	try:
		# Simplified: Just grab items below re-order level as an example for the watchdog
		low_stock = frappe.db.sql("""
			SELECT item_code, item_name, actual_qty 
			FROM `tabBin` 
			WHERE actual_qty < projected_qty AND actual_qty > 0
			LIMIT 10
		""", as_dict=True)
		
		if not low_stock:
			return
			
		settings = frappe.get_single("ApexAiAssistant Settings")
		if not settings.openai_api_key:
			return
			
		prompt = f"""You are the proactive AI Watchdog for ERPNext.
Review the following inventory stock items that are dropping low.
Draft a brief 2-sentence alert to the Procurement Manager.
Items: {json.dumps(low_stock)}"""

		import litellm
		model = settings.ai_model or "gpt-4o"
		if settings.ai_provider == "Anthropic": model = "anthropic/" + model
		
		response = litellm.completion(
			model=model,
			messages=[{"role": "user", "content": prompt}],
			api_key=settings.get_password("api_key"),
			api_base=settings.api_url if settings.api_url else None
		)
		
		alert_text = response.choices[0].message.content
		
		_send_notification("AI Watchdog: Inventory Alerts", alert_text)
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "AI Watchdog Inventory Error")

def _send_notification(subject, message):
	# Create Notification Log for Administrators
	users = frappe.get_all("Has Role", filters={"role": "System Manager", "parenttype": "User"}, pluck="parent")
	for user in users:
		log = frappe.new_doc("Notification Log")
		log.subject = subject
		log.email_content = message
		log.for_user = user
		log.insert(ignore_permissions=True)
