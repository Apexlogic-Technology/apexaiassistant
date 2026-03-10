frappe.pages['apexaiassistant-chat'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Apex Erpnext Ai Assistant'),
        single_column: true
    });

    let chat_ui = `
		<div class="apex-chat-wrapper">
			<div class="apex-history-sidebar">
				<div class="sidebar-header">
					<h6>Recent Chats</h6>
					<button class="btn btn-sm btn-action" id="apex-new-chat" title="New Chat">
						<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
							<path d="M12 5v14M5 12h14"></path>
						</svg>
					</button>
				</div>
				<div class="sidebar-list" id="apex-history-list">
					<!-- History items populated here -->
				</div>
			</div>
			
			<div class="apex-chat-container" style="margin-top:0;">
				<div class="apex-chat-messages" id="apex-messages">
					<div class="apex-message bot-message">
						<div class="message-content">Hello! How can I assist you with your ERP data today?</div>
					</div>
				</div>
				<div class="apex-chat-input-area">
					<button class="btn btn-default" id="apex-attach-btn" title="Attach File" style="border-radius: 4px 0 0 4px; border-right: none;">
						<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
							<path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
						</svg>
					</button>
					<input type="text" id="apex-input" class="form-control" placeholder="${__('Type your message here...')} (Or click mic to speak)" />
					<button id="apex-mic-btn" class="btn btn-secondary" style="border-radius: 50%; width: 50px; height: 50px; display:flex; align-items:center; justify-content:center; margin-right: 8px;" title="Voice Input">
						<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none">
							<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
							<path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
							<line x1="12" y1="19" x2="12" y2="23"></line>
							<line x1="8" y1="23" x2="16" y2="23"></line>
						</svg>
					</button>
					<button id="apex-send-btn" class="btn btn-primary">
						<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none">
							<path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"></path>
						</svg>
					</button>
				</div>
			</div>
		</div>
	`;

    $(page.main).append(chat_ui);

    let session_id = null;
    const $messages = $('#apex-messages');
    const $input = $('#apex-input');
    const $historyList = $('#apex-history-list');

    function scrollToBottom() {
        $messages.scrollTop($messages[0].scrollHeight);
    }

    function appendMessage(role, text) {
        if (!text) return;
        const msgClass = role === 'user' ? 'user-message' : 'bot-message';
        $messages.append(`
			<div class="apex-message ${msgClass}">
				<div class="message-content">${frappe.utils.escape_html(text)}</div>
			</div>
		`);
        scrollToBottom();
    }

    // Load History logic
    function loadHistory() {
        frappe.call({
            method: 'apexaiassistant.apexaiassistant.api.chat.get_sessions',
            callback: function (r) {
                if (r.message && r.message.success) {
                    $historyList.empty();
                    r.message.sessions.forEach(s => {
                        $historyList.append(`
                            <div class="history-item" data-id="${s.name}">
                                <div class="title">${s.title}</div>
                                <div class="date">${frappe.datetime.global_date_format(s.last_message_at)}</div>
                            </div>
                        `);
                    });
                }
            }
        });
    }

    $historyList.on('click', '.history-item', function () {
        const id = $(this).data('id');
        session_id = id;
        $('.history-item').removeClass('active');
        $(this).addClass('active');

        $messages.html('');

        frappe.call({
            method: 'apexaiassistant.apexaiassistant.api.chat.get_session_messages',
            args: { session_id: id },
            callback: function (r) {
                if (r.message && r.message.success) {
                    r.message.messages.forEach(msg => {
                        if (msg.role && msg.content) {
                            appendMessage(msg.role, msg.content);
                        }
                    });
                }
            }
        });
    });

    $('#apex-new-chat').on('click', function () {
        session_id = null;
        $('.history-item').removeClass('active');
        $messages.html(`
            <div class="apex-message bot-message">
                <div class="message-content">Starting a new conversation. How can I help?</div>
            </div>
        `);
    });

    function showTyping() {
        $messages.append(`
			<div class="apex-message bot-message typing-indicator" id="apex-typing">
				<div class="message-content">
					<span class="dot"></span><span class="dot"></span><span class="dot"></span>
				</div>
			</div>
		`);
        scrollToBottom();
    }

    function hideTyping() {
        $('#apex-typing').remove();
    }

    function sendMessage() {
        const message = $input.val().trim();
        if (!message) return;

        $input.val('');
        appendMessage('user', message);
        showTyping();

        frappe.call({
            method: 'apexaiassistant.apexaiassistant.api.chat.send_message',
            args: {
                message: message,
                session_id: session_id
            },
            callback: function (r) {
                hideTyping();
                if (r.message && r.message.success) {
                    const FirstTime = (session_id === null);
                    session_id = r.message.session_id;
                    const response = r.message.response;

                    appendMessage('bot', response.message);

                    if (FirstTime) loadHistory();

                    // Handle table responses for full-screen view
                    if (response.type === 'table' && response.data) {
                        renderTable(response.data);
                    } else if (response.type === 'confirmation_required') {
                        renderConfirmation(response);
                    }
                } else {
                    appendMessage('bot', 'Sorry, I encountered an error. Please try again.');
                }
            },
            error: function () {
                hideTyping();
                appendMessage('bot', 'Network error. Please check your connection.');
            }
        });
    }

    function renderTable(data) {
        const pKey = Object.keys(data)[0];
        const items = data[pKey];
        if (!items || !items.length) return;

        const keys = Object.keys(items[0]);
        let html = '<div class="apex-table-wrapper"><table class="table table-bordered table-hover"><thead><tr>';

        keys.forEach(k => html += `<th>${k}</th>`);
        html += '</tr></thead><tbody>';

        items.forEach(item => {
            html += '<tr>';
            keys.forEach(k => html += `<td>${item[k] || ''}</td>`);
            html += '</tr>';
        });

        html += '</tbody></table></div>';
        $messages.append(html);
        scrollToBottom();
    }

    function renderConfirmation(response) {
        const html = `
			<div class="apex-confirmation-box" id="confirmBox-${session_id}">
				<p><strong>Action Required:</strong> ${response.action_details.description}</p>
				<button class="btn btn-success btn-sm me-2 btn-confirm" data-action="${response.action_name}" data-params='${JSON.stringify(response.parameters)}'>Approve</button>
				<button class="btn btn-danger btn-sm btn-cancel">Cancel</button>
			</div>
		`;
        $messages.append(html);
        scrollToBottom();

        $(`#confirmBox-${session_id} .btn-confirm`).on('click', function () {
            const action = $(this).data('action');
            const params = $(this).data('params');
            $(this).parent().remove();

            showTyping();
            frappe.call({
                method: 'apexaiassistant.apexaiassistant.api.chat.confirm_action',
                args: {
                    session_id: session_id,
                    action_name: action,
                    parameters: params
                },
                callback: function (r) {
                    hideTyping();
                    if (r.message && r.message.success) {
                        appendMessage('bot', r.message.message);
                    } else {
                        appendMessage('bot', 'Action failed.');
                    }
                }
            });
        });

        $(`#confirmBox-${session_id} .btn-cancel`).on('click', function () {
            $(this).parent().remove();
            appendMessage('bot', 'Action cancelled by user.');
        });
    }

    $('#apex-send-btn').on('click', sendMessage);
    $input.on('keypress', function (e) {
        if (e.which === 13) sendMessage();
    });

    $('#apex-attach-btn').on('click', function () {
        new frappe.ui.FileUploader({
            make_attachments_public: true,
            on_success: (file_doc) => {
                const file_url = file_doc.file_url;
                const current_val = $input.val();
                $input.val(`[Attached File: ${file_url}] ${current_val}`);
                $input.focus();
                frappe.show_alert({ message: __('File uploaded successfully.'), indicator: 'green' });
            }
        });
    });

    // Voice Input Integration
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        $('#apex-mic-btn').on('click', function () {
            var $btn = $(this);
            if ($btn.hasClass('recording')) {
                recognition.stop();
                $btn.removeClass('recording').css('background', '');
                return;
            }

            recognition.start();
            $btn.addClass('recording').css('background', '#e53e3e');
            $input.attr('placeholder', __('Listening...'));
        });

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            $input.val($input.val() + " " + transcript);
            $('#apex-mic-btn').removeClass('recording').css('background', '');
            $input.attr('placeholder', __('Type your message here...'));
            sendMessage();
        };

        recognition.onerror = function (event) {
            $('#apex-mic-btn').removeClass('recording').css('background', '');
            $input.attr('placeholder', __('Voice not recognized. Type instead.'));
        };

        recognition.onend = function () {
            $('#apex-mic-btn').removeClass('recording').css('background', '');
            $input.attr('placeholder', __('Type your message here... (Or click mic to speak)'));
        };
    } else {
        $('#apex-mic-btn').hide(); // Hide if browser doesn't support Web Speech API
    }

    // Initial history load
    loadHistory();
};
