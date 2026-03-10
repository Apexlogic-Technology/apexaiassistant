# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json

class ActionRegistry:
	"""
	Registry of all allowed actions in ApexAiAssistant
	Implements whitelist approach - only registered actions can be executed
	"""
	
	def __init__(self):
		self.actions = {}
		self._load_actions()
	
	def _load_actions(self):
		"""
		Load all enabled actions from ApexAiAssistant Action Registry
		"""
		actions = frappe.get_all(
			"ApexAiAssistant Action Registry",
			filters={"enabled": 1},
			fields=["*"]
		)
		
		for action in actions:
			# Load allowed roles
			roles = frappe.get_all(
				"ApexAiAssistant Action Role",
				filters={"parent": action.name},
				fields=["role"]
			)
			action["allowed_roles"] = [r.role for r in roles]
			
			self.actions[action.action_name] = action
	
	def get_action(self, action_name):
		"""
		Get a specific action by name
		"""
		return self.actions.get(action_name)
	
	def get_available_actions(self, user_roles):
		"""
		Get all actions available to a user based on their roles
		"""
		available = []
		
		for action_name, action in self.actions.items():
			# Check if user has any of the required roles
			if not action.get("allowed_roles"):
				# If no roles specified, available to all
				available.append(action)
			else:
				# Check if user has any required role
				has_permission = any(role in user_roles for role in action["allowed_roles"])
				if has_permission:
					available.append(action)
		
		return available
	
	def is_action_allowed(self, action_name, user_roles):
		"""
		Check if an action is allowed for given user roles
		"""
		action = self.get_action(action_name)
		
		if not action:
			return False
		
		if not action.get("allowed_roles"):
			return True
		
		return any(role in user_roles for role in action["allowed_roles"])
	
	@staticmethod
	def register_default_actions():
		"""
		Register default actions for common ERPNext operations
		This should be called during installation/setup
		"""
		default_actions = [
			# Core Universal Actions
			{
				"action_name": "universal_create_document",
				"action_category": "CREATE",
				"module": "Core",
				"description": "Create a new record for ANY DocType in ERPNext not covered by a specialized action.",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "Medium",
				"handler_function": "apexaiassistant.apexaiassistant.core.document_manager.create_document",
				"allowed_roles": ["System Manager"],
				"parameters": '{"type":"object","properties":{"doctype":{"type":"string","description":"Name of the DocType"},"fields":{"type":"object","description":"Dictionary of fields and values to set"},"submit":{"type":"boolean","description":"Whether to submit the document after saving (if applicable)"}},"required":["doctype","fields"]}'
			},
			{
				"action_name": "universal_update_document",
				"action_category": "UPDATE",
				"module": "Core",
				"description": "Update an existing record for ANY DocType in ERPNext.",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "Medium",
				"handler_function": "apexaiassistant.apexaiassistant.core.document_manager.update_document",
				"allowed_roles": ["System Manager"],
				"parameters": '{"type":"object","properties":{"doctype":{"type":"string","description":"Name of the DocType"},"name":{"type":"string","description":"Name/ID of the record to update"},"fields":{"type":"object","description":"Fields to update"}},"required":["doctype","name","fields"]}'
			},
			{
				"action_name": "universal_delete_document",
				"action_category": "DELETE",
				"module": "Core",
				"description": "Delete a record for ANY DocType in ERPNext.",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "High",
				"handler_function": "apexaiassistant.apexaiassistant.core.document_manager.delete_document",
				"allowed_roles": ["System Manager"],
				"parameters": '{"type":"object","properties":{"doctype":{"type":"string","description":"Name of the DocType"},"name":{"type":"string","description":"Name/ID of the record to delete"}},"required":["doctype","name"]}'
			},
			{
				"action_name": "universal_read_document",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Read details of a specific record by its name for ANY DocType.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.document_manager.read_document",
				"allowed_roles": [],
				"parameters": '{"type":"object","properties":{"doctype":{"type":"string","description":"Name of the DocType"},"name":{"type":"string","description":"Name/ID of the record"}},"required":["doctype","name"]}'
			},
			{
				"action_name": "universal_list_documents",
				"action_category": "QUERY",
				"module": "Core",
				"description": "List or search records for ANY DocType with given filters.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.document_manager.list_documents",
				"allowed_roles": [],
				"parameters": '{"type":"object","properties":{"doctype":{"type":"string","description":"Name of the DocType"},"filters":{"type":"object","description":"Filters, e.g. {\"status\":\"Open\"}"},"fields":{"type":"array","items":{"type":"string"},"description":"Fields to fetch"},"limit":{"type":"integer","description":"Max number of records (default 20)"}},"required":["doctype"]}'
			},
			{
				"action_name": "universal_get_doctype_schema",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Get schema metadata for a given DocType to know what fields to supply for creation/update.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.document_manager.get_doctype_schema",
				"allowed_roles": [],
				"parameters": '{"type":"object","properties":{"doctype":{"type":"string","description":"Name of the DocType"}},"required":["doctype"]}'
			},
			
			# Advanced Analytics & BI
			{
				"action_name": "generate_chart_data",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Generate interactive chart data (e.g. sales_by_customer, revenue_trends).",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.advanced_tools.generate_chart_data",
				"allowed_roles": ["System Manager", "Sales Manager"],
				"parameters": '{"type":"object","properties":{"chart_type":{"type":"string","description":"bar, line, pie"},"query_type":{"type":"string","description":"e.g. sales_by_customer, revenue_trends"}},"required":["chart_type","query_type"]}'
			},
			{
				"action_name": "forecast_sales",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Forecast future sales based on historical data.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.advanced_tools.forecast_sales",
				"allowed_roles": ["System Manager", "Sales Manager"],
				"parameters": '{"type":"object","properties":{"forecast_period_days":{"type":"integer","description":"Number of days to forecast"}},"required":["forecast_period_days"]}'
			},
			{
				"action_name": "segment_customers_rfm",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Segment customers using RFM (Recency, Frequency, Monetary) Analysis.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.advanced_tools.segment_customers_rfm",
				"allowed_roles": ["System Manager", "Sales Manager"]
			},
			{
				"action_name": "predict_churn",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Predict which customers are at risk of churning.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.advanced_tools.predict_churn",
				"allowed_roles": ["System Manager", "Sales Manager"]
			},
			
			# Data Operations & Automation
			{
				"action_name": "execute_sql_query",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Execute a read-only SQL SELECT query on the ERPNext MariaDB database to fetch custom reports.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Medium",
				"handler_function": "apexaiassistant.apexaiassistant.core.nl_sql.execute_sql_query",
				"allowed_roles": ["System Manager"],
				"parameters": '{"type":"object","properties":{"query":{"type":"string","description":"Valid MySQL SELECT query"}},"required":["query"]}'
			},
			{
				"action_name": "export_query_to_csv",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Execute a SQL query and export the results to a downloadable CSV file.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Medium",
				"handler_function": "apexaiassistant.apexaiassistant.core.data_export.DataExportTools.export_query_to_csv",
				"allowed_roles": ["System Manager", "Accounts Manager"],
				"parameters": '{"type":"object","properties":{"query":{"type":"string","description":"Valid MySQL SELECT query"}},"required":["query"]}'
			},
			{
				"action_name": "search_knowledge_base",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Search the internal RAG (Retrieval-Augmented Generation) Vector database for corporate knowledge, PDFs, and policies.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.rag_engine.RAGEngine.search_knowledge_base",
				"allowed_roles": ["System Manager", "All"],
				"parameters": '{"type":"object","properties":{"query":{"type":"string","description":"The search query or question to evaluate against the knowledge base."}},"required":["query"]}'
			},
			{
				"action_name": "process_knowledge_document",
				"action_category": "UPDATE",
				"module": "Core",
				"description": "Process a newly uploaded PDF document into the AI Knowledge Base by chunking and embedding it.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Medium",
				"handler_function": "apexaiassistant.apexaiassistant.core.rag_engine.RAGEngine.process_knowledge_document",
				"allowed_roles": ["System Manager"],
				"parameters": '{"type":"object","properties":{"doc_name":{"type":"string","description":"The Name/ID of the AI Knowledge Base document to process."}},"required":["doc_name"]}'
			},
			{
				"action_name": "generate_pdf_report",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Generates a styled, downloadable PDF file from raw HTML content containing tables or textual insights. ONLY USE THIS if the user explicitly asks for a PDF.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.pdf_generator.PDFGenerator.generate_pdf_report",
				"allowed_roles": ["System Manager", "All"],
				"parameters": '{"type":"object","properties":{"html_content":{"type":"string","description":"The raw HTML payload representing the report (include <h1>, <table>, <p> tags, etc)"}, "title":{"type":"string","description":"A short title for the PDF document"}},"required":["html_content", "title"]}'
			},
			
			# Email Report Automation
			{
				"action_name": "send_email_report",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Generate and send automated email reports (sales_summary, customer_analysis, inventory_status).",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.email_reports.send_email_report",
				"allowed_roles": ["System Manager", "Sales Manager", "Stock Manager", "HR Manager"],
				"parameters": '{"type":"object","properties":{"report_type":{"type":"string","description":"sales_summary, customer_analysis, inventory_status"},"email_to":{"type":"string","description":"Email address to send to (optional)"},"from_date":{"type":"string","description":"YYYY-MM-DD"},"to_date":{"type":"string","description":"YYYY-MM-DD"}},"required":["report_type"]}'
			},
			
			# File Upload & Analysis
			{
				"action_name": "analyze_file",
				"action_category": "QUERY",
				"module": "Core",
				"description": "Analyze uploaded CSV or Excel files from the user data or public files directory.",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.file_analysis.analyze_file",
				"allowed_roles": ["System Manager", "Sales Manager", "HR Manager", "Accounts Manager", "Stock Manager"],
				"parameters": '{"type":"object","properties":{"file_url":{"type":"string","description":"URL or path to the uploaded file"},"analysis_type":{"type":"string","description":"summary, statistics, or correlations"}},"required":["file_url"]}'
			},
			
			# Deep Analytics Actions (Module Intelligence)
			{
				"action_name": "get_financial_aging_analysis",
				"action_category": "QUERY",
				"module": "Accounting",
				"description": "Get Accounts Receivable (AR) Custom Aging Analysis grouped by Customer delays",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.module_tools.ModuleIntelligenceTools.get_financial_aging_analysis",
				"allowed_roles": ["Accounts Manager", "System Manager"]
			},
			{
				"action_name": "get_manufacturing_efficiency",
				"action_category": "QUERY",
				"module": "Manufacturing",
				"description": "Analyze Manufacturing Production Efficiency based on planned vs produced quantities",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.module_tools.ModuleIntelligenceTools.get_manufacturing_efficiency",
				"allowed_roles": ["Manufacturing Manager", "System Manager"]
			},
			{
				"action_name": "get_hr_leave_balances",
				"action_category": "QUERY",
				"module": "HR",
				"description": "Get detailed Employee Leave Balances and active allocations",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.core.module_tools.ModuleIntelligenceTools.get_hr_leave_balances",
				"allowed_roles": ["HR Manager", "System Manager"]
			},
			
			# CRM Actions
			{
				"action_name": "view_leads_summary",
				"action_category": "QUERY",
				"module": "CRM",
				"description": "View summary of leads",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.crm.get_leads_summary",
				"allowed_roles": ["Sales User", "Sales Manager", "System Manager"]
			},
			{
				"action_name": "view_opportunities",
				"action_category": "QUERY",
				"module": "CRM",
				"description": "View opportunities",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.crm.get_opportunities",
				"allowed_roles": ["Sales User", "Sales Manager", "System Manager"]
			},
			
			# Selling Actions
			{
				"action_name": "view_sales_orders",
				"action_category": "QUERY",
				"module": "Selling",
				"description": "View sales orders",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.selling.get_sales_orders",
				"allowed_roles": ["Sales User", "Sales Manager", "System Manager"]
			},
			{
				"action_name": "draft_sales_order",
				"action_category": "DRAFT",
				"module": "Selling",
				"description": "Create a draft sales order",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "Medium",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.selling.create_sales_order_draft",
				"allowed_roles": ["Sales User", "Sales Manager", "System Manager"]
			},
			
			# Buying Actions
			{
				"action_name": "view_purchase_orders",
				"action_category": "QUERY",
				"module": "Buying",
				"description": "View purchase orders",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.buying.get_purchase_orders",
				"allowed_roles": ["Purchase User", "Purchase Manager", "System Manager"]
			},
			
			# Stock Actions
			{
				"action_name": "view_stock_summary",
				"action_category": "QUERY",
				"module": "Stock",
				"description": "View stock levels and summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.stock.get_stock_summary",
				"allowed_roles": ["Stock User", "Stock Manager", "System Manager"]
			},
			
			# Accounting Actions
			{
				"action_name": "view_account_balances",
				"action_category": "QUERY",
				"module": "Accounting",
				"description": "View account balances",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.accounting.get_account_balances",
				"allowed_roles": ["Accounts User", "Accounts Manager", "System Manager"]
			},
			{
				"action_name": "draft_journal_entry",
				"action_category": "DRAFT",
				"module": "Accounting",
				"description": "Create a draft journal entry",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "High",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.accounting.create_journal_entry_draft",
				"allowed_roles": ["Accounts User", "Accounts Manager", "System Manager"]
			},
			
			# HR Actions
			{
				"action_name": "view_employee_list",
				"action_category": "QUERY",
				"module": "HR",
				"description": "View employee list",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.hr.get_employee_list",
				"allowed_roles": ["HR User", "HR Manager", "System Manager"]
			},
			{
				"action_name": "approve_leave_application",
				"action_category": "APPROVE",
				"module": "HR",
				"description": "Approve a leave application",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "Medium",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.hr.approve_leave",
				"allowed_roles": ["HR Manager", "System Manager"]
			},
			
			# Payroll Actions
			{
				"action_name": "execute_payroll",
				"action_category": "EXECUTE_PAYROLL",
				"module": "Payroll",
				"description": "Execute payroll for a period",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "Critical",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.payroll.execute_payroll",
				"allowed_roles": ["HR Manager", "System Manager"]
			},
			
			# Projects Actions
			{
				"action_name": "view_projects_summary",
				"action_category": "QUERY",
				"module": "Projects",
				"description": "View projects summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.projects.get_projects_summary",
				"allowed_roles": ["Projects User", "Projects Manager", "System Manager"]
			},
			{
				"action_name": "view_tasks_summary",
				"action_category": "QUERY",
				"module": "Projects",
				"description": "View tasks summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.projects.get_tasks_summary",
				"allowed_roles": ["Projects User", "Projects Manager", "System Manager"]
			},
			
			# Manufacturing Actions
			{
				"action_name": "view_work_orders",
				"action_category": "QUERY",
				"module": "Manufacturing",
				"description": "View work orders",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.manufacturing.get_work_orders",
				"allowed_roles": ["Manufacturing User", "Manufacturing Manager", "System Manager"]
			},
			{
				"action_name": "view_bom_summary",
				"action_category": "QUERY",
				"module": "Manufacturing",
				"description": "View Bill of Materials summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.manufacturing.get_bom_summary",
				"allowed_roles": ["Manufacturing User", "Manufacturing Manager", "System Manager"]
			},
			
			# Support Actions
			{
				"action_name": "view_issues_summary",
				"action_category": "QUERY",
				"module": "Support",
				"description": "View support issues summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.support.get_issues_summary",
				"allowed_roles": ["Support Team", "System Manager"]
			},
			{
				"action_name": "view_service_level_summary",
				"action_category": "QUERY",
				"module": "Support",
				"description": "View SLA compliance summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.support.get_service_level_summary",
				"allowed_roles": ["Support Team", "System Manager"]
			},
			
			# Assets Actions
			{
				"action_name": "view_assets_summary",
				"action_category": "QUERY",
				"module": "Assets",
				"description": "View assets summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.assets.get_assets_summary",
				"allowed_roles": ["Stock User", "Accounts User", "System Manager"]
			},
			{
				"action_name": "view_asset_maintenance_schedule",
				"action_category": "QUERY",
				"module": "Assets",
				"description": "View asset maintenance schedule",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.assets.get_asset_maintenance_schedule",
				"allowed_roles": ["Stock User", "Accounts User", "System Manager"]
			},
			
			# Quality Actions
			{
				"action_name": "view_quality_inspections",
				"action_category": "QUERY",
				"module": "Quality",
				"description": "View quality inspections",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.quality.get_quality_inspections",
				"allowed_roles": ["Quality Manager", "Stock User", "System Manager"]
			},
			{
				"action_name": "view_quality_goals",
				"action_category": "QUERY",
				"module": "Quality",
				"description": "View quality goals",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.quality.get_quality_goals",
				"allowed_roles": ["Quality Manager", "System Manager"]
			},
			
			# Maintenance Actions
			{
				"action_name": "view_maintenance_schedule",
				"action_category": "QUERY",
				"module": "Maintenance",
				"description": "View maintenance schedule",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.maintenance.get_maintenance_schedule",
				"allowed_roles": ["Sales User", "System Manager"]
			},
			{
				"action_name": "view_maintenance_visits",
				"action_category": "QUERY",
				"module": "Maintenance",
				"description": "View maintenance visits",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "apexaiassistant.apexaiassistant.handlers.maintenance.get_maintenance_visits",
				"allowed_roles": ["Sales User", "System Manager"]
			},
		]
		
		for action_data in default_actions:
			# Extract roles
			roles = action_data.pop("allowed_roles", [])
			
			# Check if action already exists
			if frappe.db.exists("ApexAiAssistant Action Registry", action_data["action_name"]):
				continue
			
			# Create action
			action_doc = frappe.get_doc({
				"doctype": "ApexAiAssistant Action Registry",
				**action_data
			})
			
			# Add roles
			for role in roles:
				action_doc.append("allowed_roles", {"role": role})
			
			action_doc.insert()
		
		frappe.db.commit()
