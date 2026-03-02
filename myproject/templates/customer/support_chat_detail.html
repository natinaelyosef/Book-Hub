<!-- customer/support_chat_detail.html -->
{% extends 'customer/base.html' %}

{% block content %}
<div class="chat-fullscreen">
    <!-- Back Navigation -->
    <div class="chat-navigation">
        <a href="{% url 'support_chat_list' %}" class="back-button">
            <i class="bi bi-arrow-left"></i>
            <span>Back to Support</span>
        </a>
    </div>
    
    <!-- Main Chat Area -->
    <div class="chat-main">
        <!-- Chat Header -->
        <div class="chat-header">
            <div class="header-left">
                <div class="chat-avatar">
                    <div class="avatar-icon">
                        {% if conversation.target == 'admin' %}
                        <i class="bi bi-shield-fill-check"></i>
                        {% else %}
                        <i class="bi bi-person-badge"></i>
                        {% endif %}
                    </div>
                </div>
                
                <div class="chat-info">
                    <div class="chat-title">
                        <h3 class="chat-name">{{ conversation.subject|default:'Support Chat' }}</h3>
                        {% if conversation.issue_report %}
                        <span class="report-badge">#{{ conversation.issue_report.id }}</span>
                        {% endif %}
                    </div>
                    
                    <div class="chat-meta">
                        <span class="target-badge {{ conversation.target }}">
                            <i class="bi {% if conversation.target == 'admin' %}bi-shield{% else %}bi-person{% endif %}"></i>
                            {{ conversation.get_target_display }}
                        </span>
                        
                        {% if conversation.assigned_sub_admin %}
                        <span class="assignee-badge">
                            <i class="bi bi-person-check"></i>
                            {{ conversation.assigned_sub_admin.name }}
                        </span>
                        {% endif %}
                        
                        <span class="chat-status online">
                            <i class="bi bi-circle-fill"></i>
                            Active
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="header-right">
                <button class="header-icon-btn" id="refreshBtn">
                    <i class="bi bi-arrow-repeat"></i>
                </button>
                <button class="header-icon-btn" id="infoBtn">
                    <i class="bi bi-info-circle"></i>
                </button>
            </div>
        </div>
        
        <!-- Messages Area -->
        <div class="messages-area" id="messagesArea">
            <div class="messages-container" id="messagesContainer">
                <!-- Date Separator -->
                <div class="date-separator">
                    <span class="date-badge">Today</span>
                </div>
                
                {% for message in messages_list %}
                <div class="message-wrapper {% if message.sender_user == request.user %}message-out{% else %}message-in{% endif %}" 
                     data-message-id="{{ message.id }}"
                     data-timestamp="{{ message.created_at|date:'c' }}">
                    
                    {% if message.sender_user != request.user %}
                    <div class="message-avatar">
                        <div class="avatar-icon small">
                            <i class="bi bi-person-badge"></i>
                        </div>
                    </div>
                    {% endif %}
                    
                    <div class="message-content-wrapper">
                        <div class="message-sender">{{ message.sender_role|title }}</div>
                        
                        <div class="message-bubble">
                            {% if message.content %}
                            <div class="message-text">{{ message.content|linebreaksbr }}</div>
                            {% endif %}
                            
                            {% if message.attachment %}
                            <div class="message-attachment">
                                {% with attachment_url=message.attachment.url|lower %}
                                {% if ".jpg" in attachment_url or ".jpeg" in attachment_url or ".png" in attachment_url or ".gif" in attachment_url or ".webp" in attachment_url or ".bmp" in attachment_url or ".svg" in attachment_url %}
                                <div class="attachment-image">
                                    <img src="{{ message.attachment.url }}" alt="attachment">
                                </div>
                                <a href="{{ message.attachment.url }}" target="_blank" class="attachment-link">
                                    <i class="bi bi-eye"></i> View Image
                                </a>
                                {% else %}
                                <a href="{{ message.attachment.url }}" target="_blank" class="attachment-link">
                                    <i class="bi bi-paperclip"></i>
                                    {{ message.attachment.name|truncatechars:30 }}
                                </a>
                                {% endif %}
                                {% endwith %}
                            </div>
                            {% endif %}
                            
                            <div class="message-footer">
                                <span class="message-time">{{ message.created_at|date:'H:i' }}</span>
                                {% if message.sender_user == request.user %}
                                <span class="message-status">
                                    <i class="bi bi-check2{% if message.is_read %}-all{% endif %}"></i>
                                </span>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <!-- Scroll to bottom button -->
            <button class="scroll-bottom-btn" id="scrollBottomBtn" style="display: none;">
                <i class="bi bi-arrow-down"></i>
            </button>
        </div>
        
        <!-- Message Input Area -->
        <div class="input-area">
            <form id="support-send-form" enctype="multipart/form-data" class="message-form">
                {% csrf_token %}
                
                <div class="input-actions">
                    <button type="button" class="input-action-btn" id="attachBtn">
                        <i class="bi bi-paperclip"></i>
                    </button>
                </div>
                
                <div class="input-wrapper">
                    <textarea 
                        name="content" 
                        id="support-content" 
                        class="message-input" 
                        placeholder="Type your message..." 
                        rows="1"></textarea>
                    
                    <div class="input-tools">
                        <button type="button" class="input-tool-btn" id="emojiBtn">
                            <i class="bi bi-emoji-smile"></i>
                        </button>
                    </div>
                </div>
                
                <div class="input-attachment" id="inputAttachment" style="display: none;">
                    <span class="attachment-name" id="attachmentName"></span>
                    <button type="button" class="remove-attachment" id="removeAttachment">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
                
                <button type="submit" class="send-btn" id="sendBtn" disabled>
                    <i class="bi bi-send-fill"></i>
                </button>
            </form>
            
            <!-- Typing indicator -->
            <div class="typing-indicator" id="typingIndicator" style="display: none;">
                <span class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </span>
                <span class="typing-text">Support is typing...</span>
            </div>
        </div>
    </div>
    
    <!-- Info Sidebar (hidden by default) -->
    <div class="info-sidebar" id="infoSidebar" style="display: none;">
        <div class="info-header">
            <h3>Conversation Info</h3>
            <button class="close-info-btn" id="closeInfoBtn">
                <i class="bi bi-x-lg"></i>
            </button>
        </div>
        
        <div class="info-content">
            <div class="info-section">
                <h5>Details</h5>
                <div class="info-row">
                    <span class="info-label">Target:</span>
                    <span class="info-value target-badge {{ conversation.target }}">
                        {{ conversation.get_target_display }}
                    </span>
                </div>
                
                <div class="info-row">
                    <span class="info-label">Status:</span>
                    <span class="info-value">
                        <span class="chat-status online">
                            <i class="bi bi-circle-fill"></i> Active
                        </span>
                    </span>
                </div>
                
                {% if conversation.assigned_sub_admin %}
                <div class="info-row">
                    <span class="info-label">Assigned to:</span>
                    <span class="info-value">{{ conversation.assigned_sub_admin.name }}</span>
                </div>
                {% endif %}
                
                <div class="info-row">
                    <span class="info-label">Started:</span>
                    <span class="info-value">{{ conversation.created_at|date:'M d, Y H:i' }}</span>
                </div>
                
                {% if conversation.issue_report %}
                <div class="info-row">
                    <span class="info-label">Related Report:</span>
                    <span class="info-value">
                        <a href="#" class="report-link">#{{ conversation.issue_report.id }}</a>
                    </span>
                </div>
                {% endif %}
            </div>
            
            <div class="info-section">
                <h5>Attachments</h5>
                <div class="attachments-list" id="attachmentsList">
                    <!-- Will be populated with attachments from messages -->
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Hidden file input for attachments -->
<input type="file" id="fileInput" style="display: none;" name="attachment">

<style>
/* ===== CHAT NAVIGATION ===== */
.chat-navigation {
    padding: 1rem 2rem;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
}

.back-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 999px;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all var(--t-fast);
}

.back-button:hover {
    background: var(--primary-soft);
    color: var(--primary);
    border-color: var(--primary);
}

/* ===== CHAT MAIN ===== */
.chat-fullscreen {
    display: flex;
    flex-direction: column;
    height: calc(100vh - var(--header-h) - 2rem);
    background: var(--bg-card);
    border-radius: var(--radius-xl);
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-lg);
    margin: 1rem 0;
    position: relative;
}

.chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
}

/* Chat Header */
.chat-header {
    padding: 1rem 2rem;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow-sm);
    z-index: 10;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex: 1;
}

.chat-avatar {
    flex-shrink: 0;
}

.avatar-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    box-shadow: 0 4px 12px var(--primary-glow);
}

.avatar-icon.small {
    width: 32px;
    height: 32px;
    font-size: 1rem;
    border-radius: 10px;
}

.chat-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}

.chat-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}

.report-badge {
    padding: 0.15rem 0.6rem;
    background: var(--accent-soft);
    border-radius: 999px;
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--accent);
    border: 1px solid rgba(245,176,66,0.2);
}

.chat-meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.target-badge.admin {
    background: var(--primary-soft);
    color: var(--primary);
    border: 1px solid rgba(91,76,255,0.2);
}

.target-badge.sub_admin {
    background: var(--success-soft);
    color: var(--success);
    border: 1px solid rgba(0,201,139,0.2);
}

.assignee-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.2rem 0.6rem;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-secondary);
}

.chat-status {
    display: flex;
    align-items: center;
    gap: 0.2rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--success);
}

.chat-status i {
    font-size: 0.5rem;
}

.header-right {
    display: flex;
    gap: 0.5rem;
}

.header-icon-btn {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    cursor: pointer;
    transition: all var(--t-fast);
}

.header-icon-btn:hover {
    background: var(--primary-soft);
    color: var(--primary);
    border-color: var(--primary);
}

/* Messages Area */
.messages-area {
    flex: 1;
    overflow-y: auto;
    padding: 2rem;
    background: var(--bg-base);
    position: relative;
    scroll-behavior: smooth;
}

.messages-area::-webkit-scrollbar {
    width: 6px;
}

.messages-area::-webkit-scrollbar-track {
    background: transparent;
}

.messages-area::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 10px;
}

.messages-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 800px;
    margin: 0 auto;
}

/* Date Separator */
.date-separator {
    text-align: center;
    margin: 1rem 0;
    position: relative;
}

.date-badge {
    background: var(--bg-raised);
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.3rem 1rem;
    border-radius: 999px;
    display: inline-block;
}

/* Message Wrapper */
.message-wrapper {
    display: flex;
    gap: 0.75rem;
    animation: slideIn 0.3s ease;
}

.message-in {
    justify-content: flex-start;
}

.message-out {
    justify-content: flex-end;
}

.message-avatar {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    overflow: hidden;
    flex-shrink: 0;
    align-self: flex-end;
    margin-bottom: 0.5rem;
}

.message-content-wrapper {
    max-width: 65%;
    min-width: 200px;
}

.message-sender {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
    margin-left: 0.5rem;
}

.message-out .message-sender {
    text-align: right;
    margin-right: 0.5rem;
    color: var(--primary);
}

.message-bubble {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 0.75rem 1rem;
    box-shadow: var(--shadow-sm);
}

.message-out .message-bubble {
    background: var(--primary);
    border-color: var(--primary);
}

.message-text {
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--text-primary);
    word-wrap: break-word;
    margin-bottom: 0.5rem;
}

.message-out .message-text {
    color: white;
}

/* Attachment */
.message-attachment {
    margin-top: 0.5rem;
}

.attachment-image {
    max-width: 100%;
    max-height: 260px;
    overflow: hidden;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    margin-bottom: 0.5rem;
}

.attachment-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.attachment-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.8rem;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-decoration: none;
    transition: all var(--t-fast);
}

.attachment-link:hover {
    background: var(--primary-soft);
    color: var(--primary);
    border-color: var(--primary);
}

.message-out .attachment-link {
    background: rgba(255,255,255,0.15);
    color: white;
}

.message-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 0.25rem;
    font-size: 0.65rem;
}

.message-out .message-footer {
    color: rgba(255,255,255,0.7);
}

.message-in .message-footer {
    color: var(--text-muted);
}

.message-status i {
    font-size: 0.8rem;
}

/* Scroll bottom button */
.scroll-bottom-btn {
    position: absolute;
    bottom: 2rem;
    right: 2rem;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--primary);
    border: none;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    cursor: pointer;
    box-shadow: 0 4px 12px var(--primary-glow);
    transition: all var(--t-fast);
    z-index: 10;
}

.scroll-bottom-btn:hover {
    transform: scale(1.1);
}

/* Input Area */
.input-area {
    padding: 1rem 2rem;
    background: var(--bg-card);
    border-top: 1px solid var(--border);
    position: relative;
}

.message-form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-width: 800px;
    margin: 0 auto;
}

.input-actions {
    display: flex;
    gap: 0.25rem;
}

.input-action-btn {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all var(--t-fast);
}

.input-action-btn:hover {
    background: var(--primary-soft);
    color: var(--primary);
    border-color: var(--primary);
}

.input-wrapper {
    display: flex;
    align-items: flex-end;
    background: var(--bg-raised);
    border: 1.5px solid var(--border);
    border-radius: 24px;
    padding: 0.3rem 0.3rem 0.3rem 1rem;
    transition: all var(--t-fast);
}

.input-wrapper:focus-within {
    border-color: var(--primary);
    box-shadow: 0 0 0 4px var(--primary-soft);
}

.message-input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text-primary);
    font-family: 'Outfit', sans-serif;
    font-size: 0.9rem;
    resize: none;
    max-height: 100px;
    padding: 0.6rem 0;
    line-height: 1.5;
}

.message-input::placeholder {
    color: var(--text-muted);
}

.input-tools {
    display: flex;
    gap: 0.25rem;
    padding-right: 0.3rem;
}

.input-tool-btn {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: transparent;
    border: none;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    cursor: pointer;
    transition: all var(--t-fast);
}

.input-tool-btn:hover {
    color: var(--primary);
    background: var(--primary-soft);
}

.input-attachment {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 1rem;
    background: var(--bg-raised);
    border-radius: 999px;
    border: 1px solid var(--border);
    margin-top: 0.5rem;
}

.attachment-name {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.remove-attachment {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text-muted);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all var(--t-fast);
}

.remove-attachment:hover {
    background: var(--danger-soft);
    color: var(--danger);
    border-color: var(--danger);
}

.send-btn {
    width: 48px;
    height: 48px;
    border-radius: 16px;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    border: none;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all var(--t-fast);
    box-shadow: 0 4px 12px var(--primary-glow);
    align-self: flex-end;
}

.send-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px var(--primary-glow);
}

.send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    box-shadow: none;
}

/* Typing Indicator */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    margin-top: 0.5rem;
    color: var(--text-muted);
    font-size: 0.8rem;
}

.typing-dots {
    display: flex;
    gap: 0.2rem;
}

.typing-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--text-muted);
    animation: typing 1.4s infinite;
}

.typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typing {
    0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.5;
    }
    30% {
        transform: translateY(-4px);
        opacity: 1;
    }
}

/* Info Sidebar */
.info-sidebar {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 300px;
    background: var(--bg-card);
    border-left: 1px solid var(--border);
    box-shadow: var(--shadow-xl);
    animation: slideInRight 0.3s ease;
    z-index: 100;
    display: flex;
    flex-direction: column;
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
    }
    to {
        transform: translateX(0);
    }
}

.info-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.info-header h3 {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}

.close-info-btn {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    color: var(--text-muted);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all var(--t-fast);
}

.close-info-btn:hover {
    background: var(--danger-soft);
    color: var(--danger);
    border-color: var(--danger);
}

.info-content {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
}

.info-section {
    margin-bottom: 2rem;
}

.info-section h5 {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.info-row {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;
}

.info-label {
    width: 100px;
    font-size: 0.8rem;
    color: var(--text-muted);
}

.info-value {
    flex: 1;
    font-size: 0.8rem;
    color: var(--text-primary);
}

.report-link {
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
}

.report-link:hover {
    text-decoration: underline;
}

/* Attachments List */
.attachments-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

/* Responsive */
@media (max-width: 768px) {
    .chat-header {
        padding: 1rem;
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .header-left {
        width: 100%;
    }
    
    .chat-meta {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .message-content-wrapper {
        max-width: 85%;
    }
    
    .input-area {
        padding: 1rem;
    }
    
    .info-sidebar {
        width: 100%;
    }
}

@media (max-width: 480px) {
    .chat-avatar .avatar-icon {
        width: 40px;
        height: 40px;
        font-size: 1.2rem;
    }
    
    .chat-name {
        font-size: 1rem;
    }
    
    .message-content-wrapper {
        max-width: 90%;
    }
    
    .message-bubble {
        padding: 0.6rem 0.8rem;
    }
    
    .message-text {
        font-size: 0.85rem;
    }
    
    .input-action-btn {
        width: 36px;
        height: 36px;
    }
    
    .send-btn {
        width: 42px;
        height: 42px;
    }
}
</style>

{% endblock %}

{% block extra_js %}
<script>
(function() {
    // ===== ELEMENTS =====
    const messageArea = document.getElementById('messagesArea');
    const messagesContainer = document.getElementById('messagesContainer');
    const form = document.getElementById('support-send-form');
    const contentInput = document.getElementById('support-content');
    const sendBtn = document.getElementById('sendBtn');
    const scrollBottomBtn = document.getElementById('scrollBottomBtn');
    const attachBtn = document.getElementById('attachBtn');
    const fileInput = document.getElementById('fileInput');
    const inputAttachment = document.getElementById('inputAttachment');
    const attachmentName = document.getElementById('attachmentName');
    const removeAttachment = document.getElementById('removeAttachment');
    const infoBtn = document.getElementById('infoBtn');
    const closeInfoBtn = document.getElementById('closeInfoBtn');
    const infoSidebar = document.getElementById('infoSidebar');
    const refreshBtn = document.getElementById('refreshBtn');
    
    const sendUrl = "{% url 'support_chat_send_message' conversation.id %}";
    const pollUrlBase = "{% url 'support_chat_poll_messages' conversation.id %}";
    
    let selectedFile = null;
    let isAtBottom = true;
    
    // ===== SCROLL MANAGEMENT =====
    function scrollToBottom(animated = false) {
        if (animated) {
            messageArea.scrollTo({
                top: messageArea.scrollHeight,
                behavior: 'smooth'
            });
        } else {
            messageArea.scrollTop = messageArea.scrollHeight;
        }
    }
    
    function checkIfAtBottom() {
        const threshold = 100;
        isAtBottom = messageArea.scrollHeight - messageArea.scrollTop - messageArea.clientHeight < threshold;
        scrollBottomBtn.style.display = isAtBottom ? 'none' : 'flex';
    }
    
    messageArea.addEventListener('scroll', checkIfAtBottom);
    scrollToBottom();
    
    scrollBottomBtn.addEventListener('click', () => {
        scrollToBottom(true);
    });
    
    // ===== MESSAGE INPUT =====
    function autoResize() {
        contentInput.style.height = 'auto';
        contentInput.style.height = Math.min(contentInput.scrollHeight, 100) + 'px';
    }
    
    contentInput.addEventListener('input', function() {
        autoResize();
        sendBtn.disabled = !this.value.trim() && !selectedFile;
    });
    
    contentInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (this.value.trim() || selectedFile) {
                form.dispatchEvent(new Event('submit'));
            }
        }
    });
    
    // ===== FILE ATTACHMENT =====
    attachBtn.addEventListener('click', () => {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            selectedFile = this.files[0];
            attachmentName.textContent = selectedFile.name;
            inputAttachment.style.display = 'flex';
            sendBtn.disabled = false;
        }
    });
    
    removeAttachment.addEventListener('click', function() {
        selectedFile = null;
        fileInput.value = '';
        inputAttachment.style.display = 'none';
        sendBtn.disabled = !contentInput.value.trim();
    });
    
    // ===== SEND MESSAGE =====
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
        
        if (contentInput.value.trim()) {
            formData.append('content', contentInput.value);
        }
        
        if (selectedFile) {
            formData.append('attachment', selectedFile);
        }
        
        if (!contentInput.value.trim() && !selectedFile) return;
        
        // Disable input while sending
        contentInput.disabled = true;
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<i class="bi bi-hourglass-split"></i>';
        
        try {
            const response = await fetch(sendUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Clear form
                contentInput.value = '';
                contentInput.style.height = 'auto';
                selectedFile = null;
                fileInput.value = '';
                inputAttachment.style.display = 'none';
                
                // Append new message
                if (data.message) {
                    renderMessage(data.message);
                }
                
                scrollToBottom(true);
            } else {
                alert(data.error || 'Unable to send message.');
            }
        } catch (error) {
            alert('Message send failed.');
        } finally {
            contentInput.disabled = false;
            sendBtn.disabled = !contentInput.value.trim() && !selectedFile;
            sendBtn.innerHTML = '<i class="bi bi-send-fill"></i>';
            contentInput.focus();
        }
    });
    
    // ===== RENDER MESSAGE =====
    function renderMessage(msg) {
        if (messagesContainer.querySelector(`[data-message-id="${msg.id}"]`)) return;
        
        const isMe = msg.is_me;
        const row = document.createElement('div');
        row.className = `message-wrapper ${isMe ? 'message-out' : 'message-in'}`;
        row.dataset.messageId = msg.id;
        
        let attachmentHtml = '';
        if (msg.attachment_url) {
            if (msg.attachment_is_image) {
                attachmentHtml = `
                    <div class="message-attachment">
                        <div class="attachment-image">
                            <img src="${escapeHtml(msg.attachment_url)}" alt="attachment">
                        </div>
                        <a href="${escapeHtml(msg.attachment_url)}" target="_blank" class="attachment-link">
                            <i class="bi bi-eye"></i> View Image
                        </a>
                    </div>
                `;
            } else {
                const fileName = escapeHtml(msg.attachment_name || 'Attached file');
                attachmentHtml = `
                    <div class="message-attachment">
                        <a href="${escapeHtml(msg.attachment_url)}" target="_blank" class="attachment-link">
                            <i class="bi bi-paperclip"></i> ${fileName}
                        </a>
                    </div>
                `;
            }
        }
        
        row.innerHTML = `
            ${!isMe ? `
                <div class="message-avatar">
                    <div class="avatar-icon small">
                        <i class="bi bi-person-badge"></i>
                    </div>
                </div>
            ` : ''}
            <div class="message-content-wrapper">
                <div class="message-sender">${escapeHtml(msg.sender_role)}</div>
                <div class="message-bubble">
                    ${msg.content ? `<div class="message-text">${escapeHtml(msg.content).replace(/\n/g, '<br>')}</div>` : ''}
                    ${attachmentHtml}
                    <div class="message-footer">
                        <span class="message-time">${escapeHtml(msg.created_at)}</span>
                        ${isMe ? `
                            <span class="message-status">
                                <i class="bi bi-check2"></i>
                            </span>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(row);
        scrollToBottom();
    }
    
    // ===== POLL FOR NEW MESSAGES =====
    async function pollMessages() {
        const lastId = getLastId();
        try {
            const response = await fetch(`${pollUrlBase}?last_id=${lastId}`);
            const data = await response.json();
            
            if (data.success && data.messages) {
                data.messages.forEach(renderMessage);
            }
        } catch (error) {
            // Silent fail for polling
        }
    }
    
    function getLastId() {
        const messages = messagesContainer.querySelectorAll('[data-message-id]');
        if (!messages.length) return 0;
        return Number(messages[messages.length - 1].dataset.messageId || 0);
    }
    
    // Poll every 4 seconds
    setInterval(pollMessages, 4000);
    
    // ===== INFO SIDEBAR =====
    if (infoBtn) {
        infoBtn.addEventListener('click', () => {
            infoSidebar.style.display = 'flex';
        });
    }
    
    if (closeInfoBtn) {
        closeInfoBtn.addEventListener('click', () => {
            infoSidebar.style.display = 'none';
        });
    }
    
    // ===== REFRESH BUTTON =====
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            window.location.reload();
        });
    }
    
    // ===== EMOJI BUTTON (placeholder) =====
    document.getElementById('emojiBtn').addEventListener('click', () => {
        alert('Emoji picker would open here');
    });
    
    // ===== ESCAPE KEY HANDLER =====
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && infoSidebar.style.display === 'flex') {
            infoSidebar.style.display = 'none';
        }
    });
    
    // Helper function
    function escapeHtml(value) {
        if (!value) return '';
        const div = document.createElement('div');
        div.textContent = value;
        return div.innerHTML;
    }
    
    // Focus input on load
    contentInput.focus();
})();
</script>
{% endblock %}
