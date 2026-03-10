# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import json

def create_document(parameters, user):
	"""
	Universal create action for ANY document type in ERPNext
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		doctype = parameters.get("doctype")
		fields = parameters.get("fields", {})
		
		if not doctype:
			return {"success": False, "error": "doctype is required"}
		
		if not frappe.has_permission(doctype, "create", user=user):
			return {"success": False, "error": f"You do not have permission to create {doctype}"}
			
		doc = frappe.get_doc({
			"doctype": doctype,
			**fields
		})
		doc.insert(ignore_permissions=False)
		
		# Some doctypes require submitting to take effect
		if parameters.get("submit") and getattr(doc, "docstatus", 0) == 0:
			if hasattr(doc, "submit"):
				doc.submit()
				
		return {
			"success": True, 
			"data": {
				"name": doc.name, 
				"doctype": doc.doctype,
				"message": f"Successfully created {doctype} {doc.name}"
			}
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"Create Document Error: {parameters.get('doctype')}")
		return {"success": False, "error": str(e)}

def update_document(parameters, user):
	"""
	Universal update action for ANY document type in ERPNext
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		doctype = parameters.get("doctype")
		name = parameters.get("name")
		fields = parameters.get("fields", {})
		
		if not doctype or not name:
			return {"success": False, "error": "doctype and name are required"}
		
		if not frappe.has_permission(doctype, "write", doc=name, user=user):
			return {"success": False, "error": f"You do not have permission to update {doctype} {name}"}
			
		doc = frappe.get_doc(doctype, name)
		
		# Don't update submitted documents implicitly unless explicitly modifying allowable fields
		if doc.docstatus == 1:
			return {"success": False, "error": f"{doctype} {name} is already submitted. You cannot update it."}
			
		doc.update(fields)
		doc.save(ignore_permissions=False)
		
		return {
			"success": True, 
			"data": {
				"name": doc.name, 
				"doctype": doc.doctype,
				"message": f"Successfully updated {doctype} {doc.name}"
			}
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"Update Document Error: {parameters.get('doctype')}")
		return {"success": False, "error": str(e)}

def delete_document(parameters, user):
	"""
	Universal delete action for ANY document type in ERPNext
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		doctype = parameters.get("doctype")
		name = parameters.get("name")
		
		if not doctype or not name:
			return {"success": False, "error": "doctype and name are required"}
		
		if not frappe.has_permission(doctype, "delete", doc=name, user=user):
			return {"success": False, "error": f"You do not have permission to delete {doctype} {name}"}
			
		frappe.delete_doc(doctype, name, ignore_permissions=False)
		
		return {
			"success": True, 
			"data": {
				"message": f"Successfully deleted {doctype} {name}"
			}
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"Delete Document Error: {parameters.get('doctype')}")
		return {"success": False, "error": str(e)}

def read_document(parameters, user):
	"""
	Universal read action for ANY document type in ERPNext
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		doctype = parameters.get("doctype")
		name = parameters.get("name")
		
		if not doctype or not name:
			return {"success": False, "error": "doctype and name are required"}
		
		if not frappe.has_permission(doctype, "read", doc=name, user=user):
			return {"success": False, "error": f"You do not have permission to read {doctype} {name}"}
			
		doc = frappe.get_doc(doctype, name)
		
		return {
			"success": True, 
			"data": doc.as_dict()
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"Read Document Error: {parameters.get('doctype')}")
		return {"success": False, "error": str(e)}

def list_documents(parameters, user):
	"""
	Universal list/search action for ANY document type in ERPNext
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		doctype = parameters.get("doctype")
		filters = parameters.get("filters", {})
		fields = parameters.get("fields", ["*"])
		limit = parameters.get("limit", 20)
		
		if not doctype:
			return {"success": False, "error": "doctype is required"}
		
		if not frappe.has_permission(doctype, "read", user=user):
			return {"success": False, "error": f"You do not have permission to list {doctype}"}
			
		docs = frappe.get_list(
			doctype,
			filters=filters,
			fields=fields,
			limit_page_length=limit,
			ignore_permissions=False
		)
		
		return {
			"success": True, 
			"data": {
				"documents": docs,
				"count": len(docs)
			}
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"List Documents Error: {parameters.get('doctype')}")
		return {"success": False, "error": str(e)}

def get_doctype_schema(parameters, user):
	"""
	Get schema (fields) for a given doctype to help AI format creation payloads
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		doctype = parameters.get("doctype")
		
		if not doctype:
			return {"success": False, "error": "doctype is required"}
		
		meta = frappe.get_meta(doctype)
		fields = []
		
		for f in meta.fields:
			if f.fieldtype not in ["Section Break", "Column Break", "Tab Break", "HTML"]:
				fields.append({
					"fieldname": f.fieldname,
					"fieldtype": f.fieldtype,
					"label": f.label,
					"reqd": f.reqd,
					"options": f.options if f.fieldtype in ["Select", "Link", "Table"] else None
				})
				
		return {
			"success": True,
			"data": {
				"doctype": doctype,
				"fields": fields
			}
		}
	except Exception as e:
		return {"success": False, "error": str(e)}
