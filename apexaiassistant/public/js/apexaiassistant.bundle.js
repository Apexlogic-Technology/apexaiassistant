/**
 * ApexAiAssistant - AI Chat Interface
 * Main JavaScript file for chat functionality
 */

frappe.provide('apexaiassistant');

apexaiassistant.ChatPanel = class ChatPanel {
	constructor() {
		this.session_id = null;
		this.messages = [];
		this.is_open = false;
		this.init();
	}

	init() {
		// Add chat button to navbar
		this.add_chat_button();

		// Create chat panel
		this.create_panel();

		// Bind events
		this.bind_events();
	}

	add_chat_button() {
		// Create floating bubble instead of navbar icon
		const bubble_html = `
			<div id="apexaiassistant-chat-bubble" class="apexaiassistant-chat-bubble" title="${__('Apex Erpnext Ai')}">
				<svg class="icon" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
					<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
				</svg>
			</div>
		`;

		$('body').append(bubble_html);
	}

	create_panel() {
		const panel_html = `
			<div id="apexaiassistant-chat-panel" class="apexaiassistant-chat-panel" style="display: none;">
				<div class="chat-header">
					<h5>${__('Apex Erpnext Ai')}</h5>
					<div class="header-actions">
						<button class="btn btn-sm btn-action" id="apexaiassistant-expand-btn" title="${__('Open Full Page')}">
							<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
								<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"></path>
							</svg>
						</button>
						<button class="btn btn-sm btn-close" id="apexaiassistant-close-btn">&times;</button>
					</div>
				</div>
				<div class="chat-messages" id="apexaiassistant-messages"></div>
				<div class="chat-input-area">
					<div class="input-group">
						<button class="btn btn-default" id="apexaiassistant-attach-btn" title="${__('Attach File')}" style="border-radius: 4px 0 0 4px; border-right: none;">
							<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
								<path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
							</svg>
						</button>
						<input type="text" class="form-control" id="apexaiassistant-input" 
							placeholder="${__('Ask me anything...')}" />
						<button class="btn btn-primary" id="apexaiassistant-send-btn">
							${__('Send')}
						</button>
					</div>
				</div>
			</div>
		`;

		$('body').append(panel_html);
		this.$panel = $('#apexaiassistant-chat-panel');
		this.$messages = $('#apexaiassistant-messages');
		this.$input = $('#apexaiassistant-input');
	}

	bind_events() {
		// Toggle panel from bubble
		$(document).on('click', '#apexaiassistant-chat-bubble', () => {
			this.toggle_panel();
		});

		// Close panel
		$(document).on('click', '#apexaiassistant-close-btn', () => {
			this.close_panel();
		});

		// Expand to full page
		$(document).on('click', '#apexaiassistant-expand-btn', () => {
			frappe.set_route('apexaiassistant-chat');
			this.close_panel();
		});

		// Attach file
		$(document).on('click', '#apexaiassistant-attach-btn', () => {
			this.upload_file();
		});

		// Send message
		$(document).on('click', '#apexaiassistant-send-btn', () => {
			this.send_message();
		});

		// Send on Enter key
		this.$input.on('keypress', (e) => {
			if (e.which === 13) {
				this.send_message();
			}
		});
	}

	toggle_panel() {
		if (this.is_open) {
			this.close_panel();
		} else {
			this.open_panel();
		}
	}

	open_panel() {
		this.$panel.show();
		this.is_open = true;
		this.$input.focus();
	}

	close_panel() {
		this.$panel.hide();
		this.is_open = false;
	}

	upload_file() {
		new frappe.ui.FileUploader({
			make_attachments_public: true,
			on_success: (file_doc) => {
				const file_url = file_doc.file_url;
				const current_val = this.$input.val();
				this.$input.val(`[Attached File: ${file_url}] ${current_val}`);
				this.$input.focus();
				frappe.show_alert({ message: __('File uploaded successfully. You can now press send.'), indicator: 'green' });
			}
		});
	}

	send_message() {
		const message = this.$input.val().trim();

		if (!message) {
			return;
		}

		// Clear input
		this.$input.val('');

		// Add user message to UI
		this.add_message('user', message);

		// Show typing indicator
		this.show_typing();

		// Send to server
		frappe.call({
			method: 'apexaiassistant.apexaiassistant.api.chat.send_message',
			args: {
				message: message,
				session_id: this.session_id
			},
			callback: (r) => {
				this.hide_typing();

				if (r.message && r.message.success) {
					this.session_id = r.message.session_id;
					const response = r.message.response;

					// Add assistant response
					this.add_message('assistant', response.message);

					// Handle special response types
					if (response.type === 'confirmation_required') {
						this.show_confirmation(response);
					} else if (response.type === 'table') {
						this.show_table(response.data);
					}
				} else {
					this.add_message('assistant', 'Sorry, I encountered an error. Please try again.');
				}
			},
			error: () => {
				this.hide_typing();
				this.add_message('assistant', 'Sorry, I encountered an error. Please try again.');
			}
		});
	}

	add_message(role, content) {
		const message_class = role === 'user' ? 'user-message' : 'assistant-message';
		const message_html = `
			<div class="chat-message ${message_class}">
				<div class="message-content">${frappe.utils.escape_html(content)}</div>
			</div>
		`;

		this.$messages.append(message_html);
		this.scroll_to_bottom();
	}

	show_typing() {
		const typing_html = `
			<div class="chat-message assistant-message typing-indicator" id="typing-indicator">
				<div class="message-content">
					<span class="dot"></span>
					<span class="dot"></span>
					<span class="dot"></span>
				</div>
			</div>
		`;

		this.$messages.append(typing_html);
		this.scroll_to_bottom();
	}

	hide_typing() {
		$('#typing-indicator').remove();
	}

	show_confirmation(response) {
		const confirm_html = `
			<div class="confirmation-box">
				<p><strong>${__('Action:')} </strong>${response.action_details.description}</p>
				<div class="btn-group">
					<button class="btn btn-sm btn-success confirm-action-btn" 
						data-action="${response.action_name}"
						data-params='${JSON.stringify(response.parameters)}'>
						${__('Confirm')}
					</button>
					<button class="btn btn-sm btn-secondary cancel-action-btn">
						${__('Cancel')}
					</button>
				</div>
			</div>
		`;

		this.$messages.append(confirm_html);
		this.scroll_to_bottom();

		// Bind confirmation buttons
		$(document).on('click', '.confirm-action-btn', (e) => {
			const $btn = $(e.currentTarget);
			const action_name = $btn.data('action');
			const parameters = $btn.data('params');

			this.confirm_action(action_name, parameters);
			$btn.closest('.confirmation-box').remove();
		});

		$(document).on('click', '.cancel-action-btn', (e) => {
			$(e.currentTarget).closest('.confirmation-box').remove();
			this.add_message('assistant', 'Action cancelled.');
		});
	}

	confirm_action(action_name, parameters) {
		this.show_typing();

		frappe.call({
			method: 'apexaiassistant.apexaiassistant.api.chat.confirm_action',
			args: {
				session_id: this.session_id,
				action_name: action_name,
				parameters: parameters
			},
			callback: (r) => {
				this.hide_typing();

				if (r.message && r.message.success) {
					this.add_message('assistant', r.message.message);
				} else {
					this.add_message('assistant', 'Action failed: ' + (r.message.error || 'Unknown error'));
				}
			}
		});
	}

	show_table(data) {
		// Simple table rendering - can be enhanced
		if (data.leads || data.sales_orders || data.purchase_orders || data.stock_balances || data.accounts || data.employees) {
			const items = data.leads || data.sales_orders || data.purchase_orders || data.stock_balances || data.accounts || data.employees;

			if (items && items.length > 0) {
				const keys = Object.keys(items[0]);
				let table_html = '<table class="table table-sm table-bordered"><thead><tr>';

				keys.forEach(key => {
					table_html += `<th>${key}</th>`;
				});

				table_html += '</tr></thead><tbody>';

				items.slice(0, 10).forEach(item => {
					table_html += '<tr>';
					keys.forEach(key => {
						table_html += `<td>${item[key] || ''}</td>`;
					});
					table_html += '</tr>';
				});

				table_html += '</tbody></table>';

				if (items.length > 10) {
					table_html += `<p class="text-muted">${__('Showing 10 of')} ${items.length} ${__('records')}</p>`;
				}

				this.$messages.append(table_html);
				this.scroll_to_bottom();
			}
		}
	}

	scroll_to_bottom() {
		this.$messages.scrollTop(this.$messages[0].scrollHeight);
	}
};

// Initialize on page load
$(document).ready(function () {
	// Wait for Frappe to be ready
	if (typeof frappe !== 'undefined' && frappe.session && frappe.session.user !== 'Guest') {
		window.apexaiassistant_chat = new apexaiassistant.ChatPanel();
	} else {
		// Retry after a short delay if Frappe isn't ready yet
		setTimeout(function () {
			if (typeof frappe !== 'undefined' && frappe.session && frappe.session.user !== 'Guest') {
				window.apexaiassistant_chat = new apexaiassistant.ChatPanel();
			}
		}, 1000);
	}
});
