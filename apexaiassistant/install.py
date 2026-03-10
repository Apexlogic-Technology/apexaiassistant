# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from apexaiassistant.apexaiassistant.core.action_registry import ActionRegistry

def after_install():
	"""
	Setup ApexAiAssistant after installation
	"""
	try:
		# Create default settings only if it doesn't exist
		create_default_settings()
		
		# Register default actions
		ActionRegistry.register_default_actions()
		
		frappe.db.commit()
		
		print("=" * 60)
		print("ApexAiAssistant installation complete!")
		print("=" * 60)
		print("Next steps:")
		print("1. Go to ApexAiAssistant Settings")
		print("2. Select your AI Provider (OpenAI, Anthropic, Ollama, DeepSeek)")
		print("3. Enter your API key and save (and refresh your browser)")
		print("4. Click the chat icon to start!")
		print("=" * 60)
		
	except Exception as e:
		print(f"Installation completed with warning: {str(e)}")
		print("You can configure ApexAiAssistant Settings manually.")

def create_default_settings():
	"""
	Create default ApexAiAssistant Settings
	"""
	# Check if settings already exist
	if frappe.db.exists("ApexAiAssistant Settings", "ApexAiAssistant Settings"):
		print("ApexAiAssistant Settings already exists, skipping creation.")
		return
	
	try:
		settings = frappe.get_doc({
			"doctype": "ApexAiAssistant Settings",
			"ai_model": "gpt-4o",
			"enable_audit_log": 1,
			"max_tokens": 4000
		})
		
		# Add default enabled modules
		for module in ["CRM", "Selling", "Buying", "Stock", "Accounting", "HR", "Payroll", "Projects"]:
			settings.append("enabled_modules", {
				"module_name": module,
				"enabled": 1
			})
		
		settings.insert(ignore_permissions=True, ignore_if_duplicate=True)
		frappe.db.commit()
		print("Created default ApexAiAssistant Settings")
		
	except Exception as e:
		print(f"Could not create default settings: {str(e)}")
		print("Please create ApexAiAssistant Settings manually after installation.")
