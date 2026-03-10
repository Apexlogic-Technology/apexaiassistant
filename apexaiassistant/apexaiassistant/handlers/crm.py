# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days

def get_leads_summary(parameters, user):
	"""
	Get summary of leads with statistics
	"""
	try:
		filters = {}
		
		# Apply date filters if provided
		if parameters.get("from_date"):
			filters["creation"] = [">=", parameters["from_date"]]
		if parameters.get("to_date"):
			if "creation" in filters:
				filters["creation"] = ["between", [parameters["from_date"], parameters["to_date"]]]
			else:
				filters["creation"] = ["<=", parameters["to_date"]]
		
		# Apply status filter
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		# Apply source filter
		if parameters.get("source"):
			filters["source"] = parameters["source"]
		
		# Get leads
		leads = frappe.get_all(
			"Lead",
			filters=filters,
			fields=["name", "lead_name", "email_id", "mobile_no", "status", "source", "creation", "lead_owner", "company"],
			order_by="creation desc",
			limit=100
		)
		
		# Get summary statistics
		total_leads = len(leads)
		status_breakdown = {}
		source_breakdown = {}
		
		for lead in leads:
			status = lead.get("status", "Unknown")
			source = lead.get("source", "Unknown")
			status_breakdown[status] = status_breakdown.get(status, 0) + 1
			source_breakdown[source] = source_breakdown.get(source, 0) + 1
		
		return {
			"success": True,
			"message": f"Found {total_leads} leads",
			"data": {
				"leads": leads,
				"total": total_leads,
				"status_breakdown": status_breakdown,
				"source_breakdown": source_breakdown
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Leads Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving leads: {str(e)}",
			"error": str(e)
		}

def create_lead_draft(parameters, user):
	"""
	Create a draft lead
	"""
	try:
		# Validate required parameters
		if not parameters.get("lead_name"):
			return {
				"success": False,
				"message": "Lead name is required",
				"error": "Missing lead_name"
			}
		
		# Create lead draft
		lead = frappe.get_doc({
			"doctype": "Lead",
			"lead_name": parameters["lead_name"],
			"email_id": parameters.get("email_id"),
			"mobile_no": parameters.get("mobile_no"),
			"company_name": parameters.get("company_name"),
			"source": parameters.get("source", "Existing Customer"),
			"status": "Lead",
			"lead_owner": user
		})
		
		return {
			"success": True,
			"message": "Lead draft created. Please review and save.",
			"data": {
				"doctype": "Lead",
				"doc": lead.as_dict()
			},
			"type": "draft",
			"category": "DRAFT"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Create Lead Draft Error")
		return {
			"success": False,
			"message": f"Error creating lead draft: {str(e)}",
			"error": str(e)
		}

def convert_lead_to_customer(parameters, user):
	"""
	Convert a lead to customer
	"""
	try:
		if not parameters.get("lead"):
			return {
				"success": False,
				"message": "Lead name is required",
				"error": "Missing lead"
			}
		
		lead = frappe.get_doc("Lead", parameters["lead"])
		
		# Check if already converted
		if lead.status == "Converted":
			return {
				"success": False,
				"message": "This lead has already been converted",
				"error": "Already converted"
			}
		
		# Create customer from lead
		from erpnext.crm.doctype.lead.lead import make_customer
		customer = make_customer(parameters["lead"])
		customer.save()
		
		return {
			"success": True,
			"message": f"Lead converted to customer: {customer.name}",
			"data": {
				"customer": customer.name,
				"customer_name": customer.customer_name
			},
			"type": "action",
			"category": "APPROVE"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Convert Lead Error")
		return {
			"success": False,
			"message": f"Error converting lead: {str(e)}",
			"error": str(e)
		}

def get_lead_conversion_rate(parameters, user):
	"""
	Get lead conversion statistics
	"""
	try:
		from_date = parameters.get("from_date", add_days(getdate(), -30))
		to_date = parameters.get("to_date", getdate())
		
		# Get total leads
		total_leads = frappe.db.count("Lead", {
			"creation": ["between", [from_date, to_date]]
		})
		
		# Get converted leads
		converted_leads = frappe.db.count("Lead", {
			"creation": ["between", [from_date, to_date]],
			"status": "Converted"
		})
		
		conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
		
		# Get leads by status
		status_data = frappe.db.sql("""
			SELECT status, COUNT(*) as count
			FROM `tabLead`
			WHERE creation BETWEEN %s AND %s
			GROUP BY status
		""", (from_date, to_date), as_dict=True)
		
		return {
			"success": True,
			"message": f"Lead conversion rate: {conversion_rate:.2f}%",
			"data": {
				"total_leads": total_leads,
				"converted_leads": converted_leads,
				"conversion_rate": conversion_rate,
				"status_breakdown": status_data,
				"period": f"{from_date} to {to_date}"
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Lead Conversion Rate Error")
		return {
			"success": False,
			"message": f"Error calculating conversion rate: {str(e)}",
			"error": str(e)
		}

def get_opportunities(parameters, user):
	"""
	Get opportunities with detailed analytics
	"""
	try:
		filters = {}
		
		# Apply filters
		if parameters.get("from_date"):
			filters["creation"] = [">=", parameters["from_date"]]
		if parameters.get("to_date"):
			if "creation" in filters:
				filters["creation"] = ["between", [parameters["from_date"], parameters["to_date"]]]
			else:
				filters["creation"] = ["<=", parameters["to_date"]]
		
		if parameters.get("status"):
			filters["status"] = parameters["status"]
		
		if parameters.get("opportunity_type"):
			filters["opportunity_type"] = parameters["opportunity_type"]
		
		# Get opportunities
		opportunities = frappe.get_all(
			"Opportunity",
			filters=filters,
			fields=[
				"name", "opportunity_from", "party_name", "opportunity_amount",
				"status", "probability", "expected_closing", "opportunity_owner",
				"opportunity_type", "currency", "with_items"
			],
			order_by="expected_closing desc",
			limit=100
		)
		
		# Calculate summary
		total_amount = sum(opp.get("opportunity_amount", 0) for opp in opportunities)
		weighted_amount = sum(
			opp.get("opportunity_amount", 0) * opp.get("probability", 0) / 100
			for opp in opportunities
		)
		
		# Status breakdown
		status_breakdown = {}
		for opp in opportunities:
			status = opp.get("status", "Unknown")
			status_breakdown[status] = status_breakdown.get(status, 0) + 1
		
		return {
			"success": True,
			"message": f"Found {len(opportunities)} opportunities",
			"data": {
				"opportunities": opportunities,
				"total_count": len(opportunities),
				"total_amount": total_amount,
				"weighted_amount": weighted_amount,
				"status_breakdown": status_breakdown
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Opportunities Error")
		return {
			"success": False,
			"message": f"Error retrieving opportunities: {str(e)}",
			"error": str(e)
		}

def create_opportunity_draft(parameters, user):
	"""
	Create a draft opportunity
	"""
	try:
		# Validate required parameters
		if not parameters.get("opportunity_from") or not parameters.get("party_name"):
			return {
				"success": False,
				"message": "Opportunity source and party name are required",
				"error": "Missing required fields"
			}
		
		# Create opportunity draft
		opportunity = frappe.get_doc({
			"doctype": "Opportunity",
			"opportunity_from": parameters["opportunity_from"],
			"party_name": parameters["party_name"],
			"opportunity_type": parameters.get("opportunity_type", "Sales"),
			"opportunity_amount": parameters.get("opportunity_amount", 0),
			"probability": parameters.get("probability", 50),
			"expected_closing": parameters.get("expected_closing"),
			"contact_person": parameters.get("contact_person"),
			"opportunity_owner": user
		})
		
		return {
			"success": True,
			"message": "Opportunity draft created. Please review and save.",
			"data": {
				"doctype": "Opportunity",
				"doc": opportunity.as_dict()
			},
			"type": "draft",
			"category": "DRAFT"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Create Opportunity Draft Error")
		return {
			"success": False,
			"message": f"Error creating opportunity draft: {str(e)}",
			"error": str(e)
		}

def get_opportunity_pipeline(parameters, user):
	"""
	Get opportunity pipeline by stage
	"""
	try:
		from_date = parameters.get("from_date", add_days(getdate(), -90))
		to_date = parameters.get("to_date", getdate())
		
		# Get opportunities by status
		pipeline = frappe.db.sql("""
			SELECT 
				status,
				COUNT(*) as count,
				SUM(opportunity_amount) as total_amount,
				AVG(probability) as avg_probability,
				SUM(opportunity_amount * probability / 100) as weighted_amount
			FROM `tabOpportunity`
			WHERE expected_closing BETWEEN %s AND %s
			GROUP BY status
			ORDER BY 
				CASE status
					WHEN 'Open' THEN 1
					WHEN 'Quotation' THEN 2
					WHEN 'Converted' THEN 3
					WHEN 'Lost' THEN 4
					ELSE 5
				END
		""", (from_date, to_date), as_dict=True)
		
		total_value = sum(p.get("total_amount", 0) for p in pipeline)
		total_weighted = sum(p.get("weighted_amount", 0) for p in pipeline)
		
		return {
			"success": True,
			"message": "Opportunity pipeline analysis",
			"data": {
				"pipeline": pipeline,
				"total_value": total_value,
				"total_weighted_value": total_weighted,
				"period": f"{from_date} to {to_date}"
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Opportunity Pipeline Error")
		return {
			"success": False,
			"message": f"Error getting pipeline: {str(e)}",
			"error": str(e)
		}

def get_customer_summary(parameters, user):
	"""
	Get customer summary and analytics
	"""
	try:
		filters = {}
		
		if parameters.get("customer_group"):
			filters["customer_group"] = parameters["customer_group"]
		
		if parameters.get("territory"):
			filters["territory"] = parameters["territory"]
		
		if parameters.get("disabled") is not None:
			filters["disabled"] = parameters["disabled"]
		
		# Get customers
		customers = frappe.get_all(
			"Customer",
			filters=filters,
			fields=[
				"name", "customer_name", "customer_group", "territory",
				"customer_type", "disabled", "creation"
			],
			order_by="creation desc",
			limit=100
		)
		
		# Get revenue data for each customer
		for customer in customers:
			revenue = frappe.db.sql("""
				SELECT 
					SUM(grand_total) as total_revenue,
					COUNT(*) as order_count
				FROM `tabSales Invoice`
				WHERE customer = %s
				AND docstatus = 1
			""", customer["name"], as_dict=True)
			
			if revenue:
				customer["total_revenue"] = revenue[0].get("total_revenue", 0)
				customer["order_count"] = revenue[0].get("order_count", 0)
		
		return {
			"success": True,
			"message": f"Found {len(customers)} customers",
			"data": {
				"customers": customers,
				"total_count": len(customers)
			},
			"type": "table",
			"category": "QUERY"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Customer Summary Error")
		return {
			"success": False,
			"message": f"Error retrieving customers: {str(e)}",
			"error": str(e)
		}

