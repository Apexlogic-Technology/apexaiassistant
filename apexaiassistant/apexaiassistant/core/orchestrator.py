# Copyright (c) 2025, Apexlogic Technology and contributors
# For license information, please see license.txt

import frappe
import json
import re
import base64
import os
from apexaiassistant.apexaiassistant.core.action_registry import ActionRegistry
from apexaiassistant.apexaiassistant.core.permission_guard import PermissionGuard
from apexaiassistant.apexaiassistant.core.executor import ActionExecutor
from apexaiassistant.apexaiassistant.core.audit_logger import AuditLogger

class AIOrchestrator:
	"""
	Main orchestrator that processes user messages and coordinates
	all components of the ApexAiAssistant system
	"""
	
	def __init__(self):
		self.settings = frappe.get_single("ApexAiAssistant Settings")
		self.action_registry = ActionRegistry()
		self.permission_guard = PermissionGuard()
		self.executor = ActionExecutor()
		
		self.ai_provider = self.settings.ai_provider or "OpenAI"
		self.model = self.settings.ai_model or "gpt-4o"
		self.api_key = self.settings.get_password("api_key")
		self.api_url = self.settings.api_url
		
		if self.ai_provider != "Ollama" and not self.api_key:
			frappe.throw(f"{self.ai_provider} API Key not configured in ApexAiAssistant Settings")
	
	def process_message(self, message, session_id, user):
		"""
		Process a user message and generate a response
		"""
		try:
			# Get user roles
			user_roles = frappe.get_roles(user)
			
			# Get available actions for this user
			available_actions = self.action_registry.get_available_actions(user_roles)
			
			# Build context for AI
			system_prompt = self._build_system_prompt(user_roles, available_actions)
			
			# Get session history for context
			session_history = self._get_session_history(session_id)
			
			# Extract attached files using regex
			attached_files = re.findall(r'\[Attached File:\s*([^\]]+)\]', message)
			content = message
			
			if attached_files:
				file_path = attached_files[0].strip()
				if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
					if file_path.startswith('/private/files/'):
						physical_path = frappe.get_site_path("private", "files", file_path.split("/private/files/")[1])
					elif file_path.startswith('/files/'):
						physical_path = frappe.get_site_path("public", "files", file_path.split("/files/")[1])
					else:
						physical_path = None
						
					if physical_path and os.path.exists(physical_path):
						with open(physical_path, "rb") as image_file:
							base64_str = base64.b64encode(image_file.read()).decode('utf-8')
							mime_type = "image/jpeg"
							if file_path.lower().endswith('.png'): mime_type = "image/png"
							elif file_path.lower().endswith('.webp'): mime_type = "image/webp"
							elif file_path.lower().endswith('.gif'): mime_type = "image/gif"
							
							content = [
								{"type": "text", "text": message},
								{
									"type": "image_url",
									"image_url": {
										"url": f"data:{mime_type};base64,{base64_str}"
									}
								}
							]
							
			# Construct final messages array
			messages = [{"role": "system", "content": system_prompt}] + session_history
			messages.append({"role": "user", "content": content})
			
			# Format model string for litellm
			eval_model = self.model
			if self.ai_provider == "Anthropic":
				eval_model = "anthropic/" + eval_model
			elif self.ai_provider == "Ollama":
				eval_model = "ollama/" + eval_model
			elif self.ai_provider == "DeepSeek":
				eval_model = "deepseek/" + eval_model
			
			# Call LLM via LiteLLM
			try:
				import litellm
			except ImportError:
				frappe.throw("litellm is not installed. Run: pip install litellm")
			response = litellm.completion(
				model=eval_model,
				messages=messages,
				api_key=self.api_key,
				api_base=self.api_url if self.api_url else None,
				max_tokens=self.settings.max_tokens or 4000,
				temperature=0.7,
				functions=self._get_function_definitions(available_actions),
				function_call="auto"
			)
			
			# Process response
			choice = response.choices[0]
			
			# Check if AI wants to call a function
			message_obj = choice.message
			
			# LiteLLM normalizes function calls. We check for function_call attribute or tool_calls.
			if hasattr(message_obj, 'function_call') and message_obj.function_call:
				return self._handle_function_call(
					message_obj.function_call,
					user,
					session_id
				)
			elif hasattr(message_obj, 'tool_calls') and message_obj.tool_calls:
				# Anthropic might use tool_calls instead
				return self._handle_function_call(
					message_obj.tool_calls[0].function,
					user,
					session_id
				)
			else:
				return {
					"message": message_obj.content or "Done.",
					"type": "text",
					"action_taken": None
				}
				
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "AI Orchestrator Error")
			return {
				"message": f"I encountered an error while processing your request: {str(e)}",
				"type": "error",
				"error": str(e)
			}
	
	def _build_system_prompt(self, user_roles, available_actions):
		"""
		Build the system prompt for the AI with context about ERPNext and available actions
		"""
		actions_desc = "\n".join([
			f"- {action['name']}: {action.get('description', '')} (Category: {action['category']}, Module: {action['module']})"
			for action in available_actions
		])
		
		return f"""You are ApexAiAssistant, an AI assistant for ERPNext. You help users with their ERP tasks.

Current User Roles: {', '.join(user_roles)}

IMPORTANT RULES:
1. NEVER guess or hallucinate data. Only use data from ERPNext via the available functions.
2. Always respect user permissions. You can only perform actions the user has permission for.
3. For financial actions (POST) and payroll (EXECUTE_PAYROLL), always ask for explicit confirmation.
4. Be concise and professional in your responses.
5. When showing data, format it clearly with tables when appropriate.

AVAILABLE ACTIONS:
{actions_desc}

When a user asks about data, use the appropriate query function. When they want to create or modify something, use the appropriate action function. Always explain what you're going to do before calling a function that requires confirmation."""
	
	def _get_session_history(self, session_id):
		"""
		Get the conversation history from the session
		"""
		try:
			session = frappe.get_doc("AI Conversation", session_id)
			history = []
			
			messages = json.loads(session.messages_json or "[]")
			
			# Only include last 10 messages to avoid token limits
			for msg in messages[-10:]:
				if msg.get("role") in ["user", "assistant"] and msg.get("content"):
					history.append({
						"role": msg.get("role"),
						"content": msg.get("content")
					})
			
			return history
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "ApexAiAssistant _get_session_history Error")
			return []
	
	def _get_function_definitions(self, available_actions):
		"""
		Convert available actions to OpenAI function definitions
		"""
		functions = []
		
		for action in available_actions:
			# Parse parameters if they exist
			parameters = {"type": "object", "properties": {}, "required": []}
			
			if action.get("parameters"):
				try:
					param_def = json.loads(action["parameters"])
					parameters = param_def
				except:
					pass
			
			functions.append({
				"name": action["name"],
				"description": action.get("description", ""),
				"parameters": parameters
			})
		
		return functions if functions else None
	
	def _handle_function_call(self, function_call, user, session_id):
		"""
		Handle when AI wants to call a function
		"""
		function_name = function_call.name
		
		try:
			arguments = json.loads(function_call.arguments)
		except:
			arguments = {}
		
		# Get action details
		action = self.action_registry.get_action(function_name)
		
		if not action:
			return {
				"message": f"Action '{function_name}' is not available.",
				"type": "error"
			}
		
		# Check if action requires confirmation
		if action.get("requires_confirmation") or action.get("action_category") in ["POST", "EXECUTE_PAYROLL"]:
			return {
				"message": f"I need your confirmation to proceed with: {action.get('description', function_name)}",
				"type": "confirmation_required",
				"action_name": function_name,
				"action_details": action,
				"parameters": arguments
			}
		
		# Execute action directly
		return self.execute_action(function_name, arguments, user, session_id)
	
	def execute_action(self, action_name, parameters, user, session_id=None):
		"""
		Execute an action with permission checks
		"""
		try:
			# Get action
			action = self.action_registry.get_action(action_name)
			
			if not action:
				return {
					"success": False,
					"message": "Action not found",
					"error": "Action not found"
				}
			
			# Check permissions
			if not self.permission_guard.check_permission(user, action):
				return {
					"success": False,
					"message": "You don't have permission to perform this action",
					"error": "Permission denied"
				}
			
			# Execute action
			result = self.executor.execute(action, parameters, user)
			
			# Log action
			if self.settings.enable_audit_log:
				AuditLogger.log_action(
					user=user,
					action_name=action_name,
					action_category=action.get("action_category"),
					status="Success" if result.get("success") else "Failed",
					query=json.dumps(parameters),
					result=json.dumps(result.get("data")),
					error_message=result.get("error"),
					session_id=session_id
				)
			
			return result
			
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), f"Execute Action Error: {action_name}")
			return {
				"success": False,
				"message": f"Error executing action: {str(e)}",
				"error": str(e)
			}
