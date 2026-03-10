# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json
from apexaiassistant.apexaiassistant.core.orchestrator import AIOrchestrator

@frappe.whitelist(allow_guest=True)
def telegram_webhook():
	"""
	Receives incoming messages from standard Telegram Bot Webhooks.
	URL: /api/method/apexaiassistant.apexaiassistant.api.webhook.telegram_webhook
	"""
	try:
		data = frappe.request.get_data(as_text=True)
		payload = json.loads(data)
		
		if "message" not in payload:
			return "OK"
			
		message_text = payload["message"].get("text", "")
		chat_id = payload["message"]["chat"]["id"]
		
		# Find User by mapping a custom field or assumed matching mobile number
		# For this implementation, we assume the Telegram Chat ID is saved in User's 'mobile_no'
		user = frappe.db.get_value("User", {"mobile_no": str(chat_id)}, "name")
		
		if not user:
			# Unregistered user
			_send_telegram_reply(chat_id, "Sorry, your Telegram account is not linked to any ERPNext user.")
			return "OK"
			
		# Process Message via Orchestrator natively securely
		orchestrator = AIOrchestrator()
		session_id = f"Telegram-{chat_id}"
		
		# Ensure session exists
		if not frappe.db.exists("AI Conversation", session_id):
			doc = frappe.get_doc({
				"doctype": "AI Conversation",
				"name": session_id,
				"user": user,
				"session_title": "Telegram Bot Chat"
			})
			doc.insert(ignore_permissions=True)
			
		# Send to AI
		response = orchestrator.process_message(message_text, session_id, user)
		reply_text = response.get("message", "Processing...")
		
		_send_telegram_reply(chat_id, reply_text)
		
		return "OK"
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Telegram Webhook Error")
		return "Failed"
		

def _send_telegram_reply(chat_id, text):
	"""Sends message back to Telegram"""
	settings = frappe.get_single("ApexAiAssistant Settings")
	bot_token = settings.get("telegram_bot_token") # Add this to settings if desired
	if not bot_token:
		return
		
	import requests
	url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
	payload = {
		"chat_id": chat_id,
		"text": text
	}
	requests.post(url, json=payload)


@frappe.whitelist(allow_guest=True)
def whatsapp_webhook():
	"""
	Receives incoming messages from Twilio WhatsApp API.
	URL: /api/method/apexaiassistant.apexaiassistant.api.webhook.whatsapp_webhook
	"""
	try:
		# Twilio sends form data
		from_number = frappe.form_dict.get("From", "").replace("whatsapp:", "")
		message_text = frappe.form_dict.get("Body", "")
		
		if not from_number or not message_text:
			return "OK"
			
		user = frappe.db.get_value("User", {"mobile_no": ['like', f"%{from_number}%"]}, "name")
		
		if not user:
			return "OK" # Unregistered user
			
		orchestrator = AIOrchestrator()
		session_id = f"WhatsApp-{from_number}"
		
		if not frappe.db.exists("AI Conversation", session_id):
			doc = frappe.get_doc({"doctype": "AI Conversation", "name": session_id, "user": user, "session_title": "WhatsApp Chat"})
			doc.insert(ignore_permissions=True)
			
		response = orchestrator.process_message(message_text, session_id, user)
		reply_text = response.get("message", "Processing...")
		
		_send_whatsapp_reply(from_number, reply_text)
		
		return "OK"
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Twilio WhatsApp Error")
		return "Failed"


def _send_whatsapp_reply(to_number, text):
	settings = frappe.get_single("ApexAiAssistant Settings")
	twilio_sid = settings.get("twilio_sid") # Needs UI
	twilio_auth = settings.get("twilio_auth_token")
	twilio_from = settings.get("twilio_from_number")
	
	if not (twilio_sid and twilio_auth):
		return
		
	import requests
	url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
	auth = (twilio_sid, twilio_auth)
	data = {
		"To": f"whatsapp:{to_number}",
		"From": f"whatsapp:{twilio_from}",
		"Body": text
	}
	requests.post(url, data=data, auth=auth)
