# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe

class PermissionGuard:
	"""
	Ensures all actions respect ERPNext permissions and user roles
	"""
	
	def check_permission(self, user, action):
		"""
		Check if user has permission to execute an action
		"""
		# Get user roles
		user_roles = frappe.get_roles(user)
		
		# Check if action has role restrictions
		if not action.get("allowed_roles"):
			# No role restriction, allow all
			return True
		
		# Check if user has any of the required roles
		has_required_role = any(role in user_roles for role in action["allowed_roles"])
		
		return has_required_role
	
	def check_doctype_permission(self, user, doctype, ptype="read"):
		"""
		Check if user has permission for a specific doctype
		"""
		return frappe.has_permission(doctype, ptype, user=user)
	
	def check_document_permission(self, user, doctype, doc_name, ptype="read"):
		"""
		Check if user has permission for a specific document
		"""
		return frappe.has_permission(doctype, ptype, doc_name, user=user)
	
	def get_permitted_documents(self, user, doctype, filters=None):
		"""
		Get list of documents user has permission to access
		"""
		if not self.check_doctype_permission(user, doctype, "read"):
			return []
		
		# Use frappe.get_list which automatically applies permission filters
		return frappe.get_list(
			doctype,
			filters=filters or {},
			user=user
		)
	
	@staticmethod
	def validate_field_permissions(user, doctype, fields):
		"""
		Validate that user can access requested fields
		This is a basic implementation - can be extended based on needs
		"""
		# Get meta for doctype
		meta = frappe.get_meta(doctype)
		
		# Check each field
		accessible_fields = []
		for field in fields:
			field_meta = meta.get_field(field)
			if field_meta:
				# Basic check - can be extended with more sophisticated logic
				if not field_meta.permlevel or frappe.has_permission(doctype, "read", user=user):
					accessible_fields.append(field)
		
		return accessible_fields
