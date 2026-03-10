# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.pdf import get_pdf
import os
import uuid

class PDFGenerator:
	@staticmethod
	def generate_pdf_report(html_content, title="AI_Report"):
		"""
		Takes raw HTML content (tables, text, basic styles), converts it to a physical PDF,
		saves it to the Frappe public files directory, and returns a download link to the user.
		"""
		try:
			# Wrap the raw HTML with standard styling so it formats cleanly
			styled_html = f"""
			<!DOCTYPE html>
			<html>
			<head>
				<style>
					body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 20px; }}
					h1, h2, h3 {{ color: #1f2937; border-bottom: 1px solid #e5e7eb; padding-bottom: 10px; }}
					table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
					th, td {{ border: 1px solid #e5e7eb; padding: 12px; text-align: left; }}
					th {{ background-color: #f9fafb; font-weight: 600; color: #4b5563; }}
					p {{ line-height: 1.6; color: #374151; }}
					.footer {{ margin-top: 40px; font-size: 12px; color: #9ca3af; text-align: center; border-top: 1px solid #e5e7eb; padding-top: 20px; }}
				</style>
			</head>
			<body>
				{html_content}
				<div class="footer">Generated proactively by Apex AI Assistant</div>
			</body>
			</html>
			"""
			
			pdf_data = get_pdf(styled_html)
			
			# Generate relatively safe unique filename
			filename = f"{title.replace(' ', '_')}_{uuid.uuid4().hex[:6]}.pdf"
			file_path = frappe.get_site_path("public", "files", filename)
			
			with open(file_path, "wb") as f:
				f.write(pdf_data)
				
			return {
				"success": True,
				"message": f"Successfully generated the PDF Report. You can download it here: [Download {title}](/files/{filename})",
				"data": {"file_url": f"/files/{filename}"}
			}
			
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "AI PDF Generator Error")
			return {"success": False, "message": f"Failed to generate PDF: {str(e)}"}
