# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import importlib

class ActionExecutor:
	"""
	Executes registered actions by calling their handler functions
	"""
	
	def execute(self, action, parameters, user):
		"""
		Execute an action with given parameters
		"""
		try:
			# Get handler function
			handler_function = action.get("handler_function")
			
			if not handler_function:
				return {
					"success": False,
					"message": "No handler function defined for this action",
					"error": "Missing handler function"
				}
			
			# Parse handler function path
			# Format: module.path.function_name
			parts = handler_function.rsplit(".", 1)
			if len(parts) != 2:
				return {
					"success": False,
					"message": "Invalid handler function format",
					"error": "Invalid handler format"
				}
			
			module_path, function_name = parts
			
			# Import module and get function
			try:
				module = importlib.import_module(module_path)
				handler = getattr(module, function_name)
			except (ImportError, AttributeError) as e:
				return {
					"success": False,
					"message": f"Handler function not found: {handler_function}",
					"error": str(e)
				}
			
			# Execute handler
			result = handler(parameters, user)
			
			return result
			
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), f"Action Executor Error: {action.get('action_name')}")
			return {
				"success": False,
				"message": f"Error executing action: {str(e)}",
				"error": str(e)
			}
