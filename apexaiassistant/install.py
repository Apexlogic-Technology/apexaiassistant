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

		# Create default settings (enable all modules)
		create_default_settings()

		# Create impressive analytical Dashboard Charts
		create_default_dashboard_charts()

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
		if frappe.db.has_table("tabApexAiAssistant Action Registry"):
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

		# CSS: use .bundle.css (Frappe v15 convention)
		css_src = os.path.join(public_path, "css", "apexaiassistant.bundle.css")
		if os.path.exists(css_src):
			shutil.copy2(css_src, os.path.join(css_dest, "apexaiassistant.bundle.css"))
			print("Copied apexaiassistant.bundle.css to assets")
		else:
			print("Warning: apexaiassistant.bundle.css not found - run bench build --app apexaiassistant")

		# JS
		js_src = os.path.join(public_path, "js", "apexaiassistant.bundle.js")
		if os.path.exists(js_src):
			shutil.copy2(js_src, os.path.join(js_dest, "apexaiassistant.bundle.js"))
			print("Copied apexaiassistant.bundle.js to assets")
		else:
			print("Warning: apexaiassistant.bundle.js not found - run bench build --app apexaiassistant")

	except Exception as e:
		print(f"Warning: Could not copy assets automatically: {str(e)}")
		print("Manually copy files from apps/apexaiassistant/apexaiassistant/public/ to sites/assets/apexaiassistant/")


def create_default_settings():
	"""
	Create or update default ApexAiAssistant Settings to enable all modules
	"""
	try:
		if frappe.db.exists("ApexAiAssistant Settings", "ApexAiAssistant Settings"):
			settings = frappe.get_doc("ApexAiAssistant Settings", "ApexAiAssistant Settings")
		else:
			settings = frappe.get_doc({
				"doctype": "ApexAiAssistant Settings",
				"ai_model": "gpt-4o",
				"enable_audit_log": 1,
				"max_tokens": 4000
			})

		# Clear existing modules to avoid duplicates
		settings.set("enabled_modules", [])

		# All standard ERPNext modules including HR
		modules_to_enable = [
			"Core", "CRM", "Selling", "Buying", "Stock",
			"Accounting", "HR", "Payroll", "Projects",
			"Manufacturing", "Support", "Assets", "Quality", "Maintenance"
		]

		for module in modules_to_enable:
			settings.append("enabled_modules", {
				"module_name": module,
				"enabled": 1
			})

		settings.save(ignore_permissions=True)
		frappe.db.commit()
		print("Populated all standard enabled_modules in ApexAiAssistant Settings")

	except Exception as e:
		print(f"Could not create default settings: {str(e)}")
		print("Please create ApexAiAssistant Settings manually after installation.")


def create_default_dashboard_charts():
	"""
	Creates predictive and descriptive Dashboard Charts
	that hook into the custom python analytics methods.
	"""
	charts = [
		{
			"doctype": "Dashboard Chart",
			"chart_name": "AI Revenue Regression Forecast",
			"chart_type": "Custom",
			"source": "apexaiassistant.apexaiassistant.core.analytics.get_revenue_regression",
			"type": "Line",
			"color": "#667eea",
			"dynamic_filters_json": "[]",
			"is_public": 1,
			"is_standard": 1,
			"module": "ApexAiAssistant"
		},
		{
			"doctype": "Dashboard Chart",
			"chart_name": "AI Employee Attrition Prediction Risk",
			"chart_type": "Custom",
			"source": "apexaiassistant.apexaiassistant.core.analytics.get_attrition_forecast",
			"type": "Bar",
			"color": "#fc4f4f",
			"dynamic_filters_json": "[]",
			"is_public": 1,
			"is_standard": 1,
			"module": "ApexAiAssistant"
		},
		{
			"doctype": "Dashboard Chart",
			"chart_name": "AI Token Usage (Last 14 Days)",
			"chart_type": "Custom",
			"source": "apexaiassistant.apexaiassistant.core.analytics.get_ai_token_usage",
			"type": "Line",
			"color": "#38bdf8",
			"dynamic_filters_json": "[]",
			"is_public": 1,
			"is_standard": 1,
			"module": "ApexAiAssistant"
		}
	]

	print("Generating Advanced Analytical Dashboard Charts...")
	for chart_data in charts:
		if not frappe.db.exists("Dashboard Chart", chart_data["chart_name"]):
			try:
				doc = frappe.get_doc(chart_data)
				doc.insert(ignore_permissions=True)
			except Exception as e:
				print(f"Warning: Failed to create chart {chart_data['chart_name']}: {str(e)}")
	frappe.db.commit()
