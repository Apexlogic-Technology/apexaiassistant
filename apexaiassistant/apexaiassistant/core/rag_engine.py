# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json
import numpy as np
import os
import PyPDF2
from litellm import embedding
from apexaiassistant.apexaiassistant.core.orchestrator import AIOrchestrator

class RAGEngine:
	@staticmethod
	def process_knowledge_document(doc_name, user=None):
		"""
		Reads an uploaded PDF from an AI Knowledge Base document,
		extracts text, chunks it, generates embeddings, and saves them.
		"""
		try:
			kb_doc = frappe.get_doc("AI Knowledge Base", doc_name)
			
			if not kb_doc.document_file:
				return {"success": False, "message": "No file attached to this knowledge base document."}
			
			kb_doc.db_set('status', 'Processing')
			
			# Get physical file path
			file_url = kb_doc.document_file
			if file_url.startswith("/private/files/"):
				file_path = frappe.get_site_path("private", "files", file_url.split("/private/files/")[1])
			elif file_url.startswith("/files/"):
				file_path = frappe.get_site_path("public", "files", file_url.split("/files/")[1])
			else:
				return {"success": False, "message": "Unknown file path format."}

			if not os.path.exists(file_path):
				kb_doc.db_set('status', 'Failed')
				return {"success": False, "message": f"File not found on disk at {file_path}"}
				
			# Extract Text using PyPDF2
			text_content = ""
			if file_path.lower().endswith(".pdf"):
				with open(file_path, "rb") as f:
					reader = PyPDF2.PdfReader(f)
					for page in reader.pages:
						extracted = page.extract_text()
						if extracted:
							text_content += extracted + "\n"
			elif file_path.lower().endswith(".txt") or file_path.lower().endswith(".csv"):
				with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
					text_content = f.read()
			else:
				kb_doc.db_set('status', 'Failed')
				return {"success": False, "message": "Unsupported file format for Knowledge Base extraction."}
				
			if not text_content.strip():
				kb_doc.db_set('status', 'Failed')
				return {"success": False, "message": "No text could be extracted from the document."}

			# Chunking Logic (Simple character chunk overlap)
			chunk_size = 1500
			overlap = 200
			chunks = []
			start = 0
			while start < len(text_content):
				end = start + chunk_size
				chunks.append(text_content[start:end])
				start += chunk_size - overlap

			# Get settings for Provider
			settings = frappe.get_single('ApexAiAssistant Settings')
			api_key = settings.openai_api_key
			model = "text-embedding-ada-002" # Hardcoded proxy fallback standard for embeddings
			
			# Delete old chunks if re-processing
			frappe.db.delete("AI Knowledge Chunk", {"parent_document": doc_name})
			
			# Generate Embeddings and Save
			for i, chunk in enumerate(chunks):
				response = embedding(model=model, input=[chunk], api_key=api_key)
				vector = response['data'][0]['embedding']
				
				chunk_doc = frappe.get_doc({
					"doctype": "AI Knowledge Chunk",
					"parent_document": doc_name,
					"chunk_index": i,
					"text_content": chunk,
					"embedding_vector": json.dumps(vector)
				})
				chunk_doc.insert(ignore_permissions=True)
				
			kb_doc.db_set('total_chunks', len(chunks))
			kb_doc.db_set('status', 'Completed')
			frappe.db.commit()
			
			return {"success": True, "message": f"Successfully processed '{kb_doc.title}' into {len(chunks)} knowledge chunks."}

		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "RAG Engine Processing Error")
			return {"success": False, "message": str(e)}

	@staticmethod
	def search_knowledge_base(query, user=None):
		"""
		Searches the vector embeddings across all AI Knowledge Chunks
		and returns the top 3 contextual chunks.
		"""
		try:
			settings = frappe.get_single('ApexAiAssistant Settings')
			api_key = settings.openai_api_key
			model = "text-embedding-ada-002"
			
			# Generate embedding for the search query
			query_embedding_res = embedding(model=model, input=[query], api_key=api_key)
			query_vector = np.array(query_embedding_res['data'][0]['embedding'])
			
			# Fetch all completed chunks (In a production system with 10M+ rows, you would use pgvector or chromadb)
			# For Frappe standard compatibility, we do in-memory dot product for small MB knowledge bases
			chunks = frappe.db.sql("""
				SELECT name, parent_document, text_content, embedding_vector 
				FROM `tabAI Knowledge Chunk`
			""", as_dict=True)
			
			if not chunks:
				return {
					"message": "The Knowledge Base is empty. Cannot retrieve context.",
					"success": True,
					"context": []
				}
				
			results = []
			for c in chunks:
				if c.embedding_vector:
					v = np.array(json.loads(c.embedding_vector))
					# Cosine Similarity
					similarity = np.dot(query_vector, v) / (np.linalg.norm(query_vector) * np.linalg.norm(v))
					results.append({
						"parent": c.parent_document,
						"content": c.text_content,
						"score": float(similarity)
					})
					
			# Sort by similarity descending
			results.sort(key=lambda x: x['score'], reverse=True)
			
			# Take Top 3
			top_results = results[:3]
			
			formatted_context = "CRITICAL RAG KNOWLEDGE RETRIEVED:\n\n"
			for i, r in enumerate(top_results):
				formatted_context += f"--- Source Document: {r['parent']} (Relevance: {round(r['score']*100, 1)}%) ---\n"
				formatted_context += f"{r['content']}\n\n"
				
			return {
				"message": "Retrieved semantic knowledge base context successfully.",
				"data": {"knowledge_context": formatted_context},
				"success": True
			}
			
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "RAG Search Error")
			return {"success": False, "message": f"Vector Search failed: {str(e)}"}
