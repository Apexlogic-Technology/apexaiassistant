# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_days, getdate, nowdate, formatdate
import json

def send_email_report(parameters, user):
	"""
	Automatically generates and sends formatted email reports
	"""
	try:
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
			
		report_type = parameters.get("report_type")
		email_to = parameters.get("email_to")
		from_date = parameters.get("from_date")
		to_date = parameters.get("to_date")
		
		if not email_to:
			# Default to user's email if none provided
			email_to = frappe.db.get_value("User", user, "email")
			if not email_to:
				return {"success": False, "error": "Email address is required."}
		
		if not from_date:
			from_date = add_days(nowdate(), -30) # Default to last 30 days
		if not to_date:
			to_date = nowdate()

		subject = f"{report_type.replace('_', ' ').title()} Report"
		html_content = ""

		if report_type == "sales_summary":
			html_content = _generate_sales_summary(from_date, to_date)
		elif report_type == "customer_analysis":
			html_content = _generate_customer_analysis()
		elif report_type == "inventory_status":
			html_content = _generate_inventory_status()
		else:
			return {"success": False, "error": f"Unsupported report type: {report_type}"}

		# Send the email using Frappe's email queue
		frappe.sendmail(
			recipients=[email_to],
			subject=subject,
			message=html_content,
			now=True
		)

		return {
			"success": True,
			"data": {
				"message": f"Successfully generated and triggered {report_type} email to {email_to}",
				"report_preview": html_content[:200] + "..." # Just for AI to confirm it generated something
			}
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Email Report Generation Error")
		return {"success": False, "error": f"Failed to send email: {str(e)}"}

def _generate_sales_summary(from_date, to_date):
	# Calculate totals
	data = frappe.db.sql('''
		SELECT 
			COUNT(name) as order_count, 
			SUM(base_grand_total) as revenue 
		FROM `tabSales Invoice` 
		WHERE docstatus = 1 AND posting_date BETWEEN %s AND %s
	''', (from_date, to_date), as_dict=True)[0]
	
	revenue = data.revenue or 0.0
	order_count = data.order_count or 0
	
	# Top customers
	top_customers = frappe.db.sql('''
		SELECT customer, SUM(base_grand_total) as total 
		FROM `tabSales Invoice` 
		WHERE docstatus = 1 AND posting_date BETWEEN %s AND %s
		GROUP BY customer 
		ORDER BY total DESC LIMIT 5
	''', (from_date, to_date), as_dict=True)
	
	html = f"<h2>Sales Summary ({formatdate(from_date)} to {formatdate(to_date)})</h2>"
	html += f"<p><strong>Total Revenue:</strong> {frappe.utils.fmt_money(revenue)}</p>"
	html += f"<p><strong>Total Orders:</strong> {order_count}</p>"
	
	html += "<h3>Top 5 Customers</h3><ul>"
	for c in top_customers:
		html += f"<li>{c.customer}: {frappe.utils.fmt_money(c.total)}</li>"
	html += "</ul>"
	
	return html

def _generate_customer_analysis():
	# Total customers
	total = frappe.db.count("Customer")
	
	# Active customers in last 90 days
	active = frappe.db.sql('''
		SELECT COUNT(DISTINCT customer) as count
		FROM `tabSales Invoice`
		WHERE docstatus = 1 AND posting_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
	''')[0][0]
	
	html = "<h2>Customer Analysis</h2>"
	html += f"<p><strong>Total Customers:</strong> {total}</p>"
	html += f"<p><strong>Active Customers (90 days):</strong> {active}</p>"
	
	if total > 0:
		html += f"<p><strong>Active Percentage:</strong> {round((active/total)*100, 1)}%</p>"
	
	return html

def _generate_inventory_status():
	# Low stock items logic
	low_stock = frappe.db.sql('''
		SELECT item_code, projected_qty, re_order_level 
		FROM `tabBin` 
		WHERE projected_qty < re_order_level AND re_order_level > 0
		LIMIT 10
	''', as_dict=True)
	
	html = "<h2>Inventory Status</h2>"
	if not low_stock:
		html += "<p>All items are above re-order levels.</p>"
	else:
		html += "<h3>Low Stock Alerts (Top 10)</h3><ul>"
		for item in low_stock:
			html += f"<li>{item.item_code} - Current: {item.projected_qty}, Re-order Level: {item.re_order_level}</li>"
		html += "</ul>"
		
	return html

class EmailReportAutomation:
	@staticmethod
	def send_daily_reports():
		users = frappe.get_all("User", filters={"enabled": 1}, fields=["name"])
		for u in users:
			if "Sales Manager" in frappe.get_roles(u.name):
				send_email_report({"report_type": "sales_summary", "email_to": u.name}, u.name)
				
	@staticmethod
	def send_weekly_reports():
		users = frappe.get_all("User", filters={"enabled": 1}, fields=["name"])
		for u in users:
			if "HR Manager" in frappe.get_roles(u.name) or "System Manager" in frappe.get_roles(u.name):
				send_email_report({"report_type": "customer_analysis", "email_to": u.name}, u.name)
				
	@staticmethod
	def send_monthly_reports():
		users = frappe.get_all("User", filters={"enabled": 1}, fields=["name"])
		for u in users:
			if "Stock Manager" in frappe.get_roles(u.name):
				send_email_report({"report_type": "inventory_status", "email_to": u.name}, u.name)
