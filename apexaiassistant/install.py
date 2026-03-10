# Copyright (c) 2025, Apexlogic Technology and contributors
# For license information, please see license.txt

import os
import shutil
import frappe

def after_install():
	"""
	Setup ApexAiAssistant after installation
	"""
	try:
		# Copy pre-built assets to sites assets directory
		install_assets()

		# Create default settings only if it doesn't exist
		create_default_settings()
		
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

def after_migrate():
	"""
	Run after bench migrate - registers default actions once all DocTypes are synced.
	"""
	try:
		from apexaiassistant.apexaiassistant.core.action_registry import ActionRegistry
		if frappe.db.table_exists("ApexAiAssistant Action Registry"):
			ActionRegistry.register_default_actions()
			frappe.db.commit()
	except Exception as e:
		print(f"Could not register default actions: {str(e)}")

def install_assets():
	"""
	Copy pre-built frontend assets from public/ into sites/assets/apexaiassistant/
	so they are served correctly without requiring a build step.
	"""
	try:
		app_path = frappe.get_app_path("apexaiassistant")
		public_path = os.path.join(app_path, "public")
		bench_path = frappe.utils.get_bench_path()
		assets_path = os.path.join(bench_path, "sites", "assets", "apexaiassistant")

		css_dest = os.path.join(assets_path, "css")
		js_dest = os.path.join(assets_path, "js")
		os.makedirs(css_dest, exist_ok=True)
		os.makedirs(js_dest, exist_ok=True)

		css_src = os.path.join(public_path, "css", "apexaiassistant.css")
		if os.path.exists(css_src):
			shutil.copy2(css_src, os.path.join(css_dest, "apexaiassistant.css"))
			print("Copied apexaiassistant.css to assets")

		js_src = os.path.join(public_path, "js", "apexaiassistant.bundle.js")
		if os.path.exists(js_src):
			shutil.copy2(js_src, os.path.join(js_dest, "apexaiassistant.bundle.js"))
			print("Copied apexaiassistant.bundle.js to assets")

	except Exception as e:
		print(f"Warning: Could not copy assets automatically: {str(e)}")
		print("Manually copy files from apps/apexaiassistant/apexaiassistant/public/ to sites/assets/apexaiassistant/")

def create_default_settings():
	"""
	Create default ApexAiAssistant Settings
	"""
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

