# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AIKnowledgeBase(Document):
	def after_insert(self):
		if self.document_file:
			frappe.enqueue(
				"apexaiassistant.apexaiassistant.core.rag_engine.RAGEngine.process_knowledge_document",
				doc_name=self.name,
				queue="long"
			)
