# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ApexAiAssistantChatSession(Document):
	def before_save(self):
		if not self.created_at:
			self.created_at = frappe.utils.now()
		self.last_message_at = frappe.utils.now()
