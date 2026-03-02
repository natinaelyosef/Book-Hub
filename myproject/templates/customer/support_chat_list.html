<!-- customer/support_chat_list.html -->
{% extends 'customer/base.html' %}

{% block content %}
<div class="support-fullscreen">
    <!-- Sidebar - New Chat Form -->
    <div class="support-sidebar">
        <div class="sidebar-header">
            <div class="header-icon">
                <i class="bi bi-headset"></i>
            </div>
            <h2 class="sidebar-title">Support Center</h2>
            <p class="sidebar-subtitle">We're here to help</p>
        </div>
        
        <div class="new-chat-form">
            <form method="post" action="{% url 'support_chat_start' %}" enctype="multipart/form-data" id="newChatForm">
                {% csrf_token %}
                
                <div class="form-group">
                    <label class="form-label">
                        <i class="bi bi-shield-check"></i>
                        Contact
                    </label>
                    <select name="target" class="form-control">
                        {% for value,label in target_choices %}
                        <option value="{{ value }}">{{ label }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">
                        <i class="bi bi-flag"></i>
                        Related Report
                    </label>
                    <select name="issue_report_id" class="form-control">
                        <option value="">No linked report</option>
                        {% for report in open_reports %}
                        <option value="{{ report.id }}">Report #{{ report.id }} - {{ report.get_status_display }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">
                        <i class="bi bi-tag"></i>
                        Subject
                    </label>
                    <input type="text" name="subject" class="form-control" placeholder="Brief description...">
                </div>
                
                <div class="form-group">
                    <label class="form-label">
                        <i class="bi bi-chat-text"></i>
                        Message
                    </label>
                    <textarea class="form-control" name="message" rows="4" placeholder="How can we help you?"></textarea>
                </div>
                
                <div class="form-group">
                    <label class="form-label file-upload" id="fileUploadLabel">
                        <i class="bi bi-paperclip"></i>
                        Attach File
                        <input type="file" name="attachment" class="file-input" id="fileInput">
                    </label>
                    <div class="file-preview" id="filePreview"></div>
                </div>
                
                <button type="submit" class="submit-btn">
                    <i class="bi bi-send-fill"></i>
                    Start Support Chat
                </button>
            </form>
        </div>
    </div>
    
    <!-- Main Area - Conversations List -->
    <div class="support-main">
        <div class="main-header">
            <div class="header-left">
                <h1 class="main-title">Support Conversations</h1>
                <span class="unread-badge-large" id="totalUnreadBadge">
                    {{ total_unread }} unread
                </span>
            </div>
            
            <div class="header-right">
                <div class="search-wrapper">
                    <i class="bi bi-search"></i>
                    <input type="text" placeholder="Search conversations..." id="searchConversations" class="search-input">
                </div>
            </div>
        </div>
        
        <div class="conversations-list" id="conversationsList">
            {% for row in conversation_rows %}
            <a href="{% url 'support_chat_detail' row.conversation.id %}" 
               class="conversation-card {% if row.unread_count %}unread{% endif %}"
               data-conversation-id="{{ row.conversation.id }}"
               data-search-text="{{ row.conversation.subject|default:'' }} {{ row.last_message.content|default:'' }}">
                
                <div class="conversation-avatar">
                    <div class="avatar-icon">
                        {% if row.conversation.target == 'admin' %}
                        <i class="bi bi-shield-fill-check"></i>
                        {% else %}
                        <i class="bi bi-person-badge"></i>
                        {% endif %}
                    </div>
                </div>
                
                <div class="conversation-content">
                    <div class="conversation-header">
                        <div class="conversation-title">
                            <span class="conversation-subject">
                                {{ row.conversation.subject|default:'Support conversation' }}
                            </span>
                            {% if row.conversation.issue_report %}
                            <span class="report-badge">
                                #{{ row.conversation.issue_report.id }}
                            </span>
                            {% endif %}
                        </div>
                        <div class="conversation-time">
                            {{ row.conversation.updated_at|date:'H:i' }}
                        </div>
                    </div>
                    
                    <div class="conversation-meta">
                        <div class="meta-badges">
                            <span class="target-badge {{ row.conversation.target }}">
                                <i class="bi {% if row.conversation.target == 'admin' %}bi-shield{% else %}bi-person{% endif %}"></i>
                                {{ row.conversation.get_target_display }}
                            </span>
                            {% if row.conversation.assigned_sub_admin %}
                            <span class="assignee-badge">
                                <i class="bi bi-person-check"></i>
                                {{ row.conversation.assigned_sub_admin.name }}
                            </span>
                            {% endif %}
                        </div>
                    </div>
                    
                    <div class="conversation-preview">
                        <div class="preview-text">
                            {% if row.last_message %}
                                {{ row.last_message.content|truncatechars:80 }}
                            {% else %}
                                <span class="no-messages">No messages yet</span>
                            {% endif %}
                        </div>
                        
                        <div class="preview-meta">
                            {% if row.unread_count %}
                            <span class="unread-badge">{{ row.unread_count }}</span>
                            {% endif %}
                            <span class="message-time">{{ row.conversation.updated_at|date:'M d' }}</span>
                        </div>
                    </div>
                </div>
            </a>
            {% empty %}
            <div class="empty-state">
                <div class="empty-icon">
                    <i class="bi bi-chat-dots"></i>
                </div>
                <h3>No support conversations</h3>
                <p>Start a new support chat using the form on the left</p>
            </div>
            {% endfor %}
        </div>
    </div>
</div>

<style>
/* ===== FULLSCREEN SUPPORT LAYOUT ===== */
.support-fullscreen {
    display: flex;
    height: calc(100vh - var(--header-h) - 2rem);
    background: var(--bg-base);
    border-radius: var(--radius-xl);
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-lg);
    margin: 1rem 0;
}

/* ===== SIDEBAR ===== */
.support-sidebar {
    width: 380px;
    background: linear-gradient(145deg, var(--bg-card), var(--bg-raised));
    border-right: 1px solid var(--border);
    overflow-y: auto;
    padding: 2rem 1.5rem;
}

.sidebar-header {
    text-align: center;
    margin-bottom: 2rem;
}

.header-icon {
    width: 64px;
    height: 64px;
    border-radius: 20px;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    color: white;
    font-size: 2rem;
    box-shadow: 0 8px 20px var(--primary-glow);
}

.sidebar-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}

.sidebar-subtitle {
    font-size: 0.85rem;
    color: var(--text-muted);
}

/* New Chat Form */
.new-chat-form {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
}

.form-group {
    margin-bottom: 1.25rem;
}

.form-label {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
}

.form-label i {
    color: var(--primary);
    font-size: 0.9rem;
}

.form-control {
    width: 100%;
    padding: 0.7rem 1rem;
    border-radius: var(--radius);
    border: 1.5px solid var(--border);
    background: var(--bg-raised);
    color: var(--text-primary);
    font-size: 0.9rem;
    transition: all var(--t-fast);
}

.form-control:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 4px var(--primary-soft);
}

textarea.form-control {
    resize: vertical;
    min-height: 100px;
    font-family: 'Outfit', sans-serif;
}

/* File Upload */
.file-upload {
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1rem;
    background: var(--bg-raised);
    border: 1.5px dashed var(--border);
    border-radius: var(--radius);
    color: var(--text-secondary);
    font-size: 0.9rem;
    cursor: pointer;
    transition: all var(--t-fast);
}

.file-upload:hover {
    border-color: var(--primary);
    background: var(--primary-soft);
}

.file-input {
    position: absolute;
    opacity: 0;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    cursor: pointer;
}

.file-preview {
    margin-top: 0.5rem;
    padding: 0.5rem;
    background: var(--bg-raised);
    border-radius: var(--radius-sm);
    font-size: 0.8rem;
    color: var(--text-secondary);
    display: none;
}

.file-preview.active {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.file-preview i {
    color: var(--success);
}

.submit-btn {
    width: 100%;
    padding: 0.9rem;
    border-radius: var(--radius);
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    border: none;
    color: white;
    font-size: 0.9rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    cursor: pointer;
    transition: all var(--t-fast);
    box-shadow: 0 4px 12px var(--primary-glow);
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px var(--primary-glow);
}

/* ===== MAIN AREA ===== */
.support-main {
    flex: 1;
    background: var(--bg-card);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.main-header {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    background: var(--bg-card);
}

.header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.main-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin: 0;
}

.unread-badge-large {
    background: var(--danger);
    color: white;
    padding: 0.3rem 1rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    box-shadow: 0 4px 12px rgba(255,77,109,0.3);
}

.search-wrapper {
    display: flex;
    align-items: center;
    background: var(--bg-raised);
    border: 1.5px solid var(--border);
    border-radius: 999px;
    padding: 0.3rem 0.3rem 0.3rem 1rem;
    width: 280px;
}

.search-wrapper i {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-right: 0.5rem;
}

.search-input {
    flex: 1;
    border: none;
    background: transparent;
    outline: none;
    color: var(--text-primary);
    font-size: 0.9rem;
    padding: 0.6rem 0;
}

.search-input::placeholder {
    color: var(--text-muted);
}

/* Conversations List */
.conversations-list {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem 2rem;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
}

.conversations-list::-webkit-scrollbar {
    width: 6px;
}

.conversations-list::-webkit-scrollbar-track {
    background: transparent;
}

.conversations-list::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 10px;
}

/* Conversation Card */
.conversation-card {
    display: flex;
    gap: 1rem;
    padding: 1.25rem;
    border-radius: var(--radius-lg);
    background: var(--bg-card);
    border: 1px solid var(--border);
    margin-bottom: 0.75rem;
    text-decoration: none;
    color: inherit;
    transition: all var(--t-fast);
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.conversation-card:hover {
    transform: translateX(4px);
    border-color: var(--primary);
    box-shadow: var(--shadow);
}

.conversation-card.unread {
    background: var(--primary-soft);
    border-left: 3px solid var(--primary);
}

/* Avatar */
.conversation-avatar {
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

.conversation-card.unread .avatar-icon {
    box-shadow: 0 0 0 3px rgba(91,76,255,0.3);
}

/* Content */
.conversation-content {
    flex: 1;
    min-width: 0;
}

.conversation-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.4rem;
}

.conversation-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.conversation-subject {
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-primary);
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

.conversation-time {
    font-size: 0.7rem;
    color: var(--text-muted);
    white-space: nowrap;
}

/* Meta badges */
.conversation-meta {
    margin-bottom: 0.5rem;
}

.meta-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.target-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
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
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-secondary);
}

/* Preview */
.conversation-preview {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
}

.preview-text {
    font-size: 0.85rem;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
}

.no-messages {
    color: var(--text-muted);
    font-style: italic;
}

.preview-meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-shrink: 0;
}

.unread-badge {
    background: var(--primary);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    min-width: 20px;
    height: 20px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 6px;
    box-shadow: 0 4px 8px var(--primary-glow);
}

.message-time {
    font-size: 0.7rem;
    color: var(--text-muted);
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
}

.empty-icon {
    font-size: 4rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
    opacity: 0.3;
}

.empty-state h3 {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.empty-state p {
    font-size: 0.9rem;
    color: var(--text-secondary);
}

/* Responsive */
@media (max-width: 1024px) {
    .support-sidebar {
        width: 340px;
    }
    
    .search-wrapper {
        width: 240px;
    }
}

@media (max-width: 768px) {
    .support-fullscreen {
        flex-direction: column;
        height: auto;
        min-height: calc(100vh - var(--header-h) - 2rem);
    }
    
    .support-sidebar {
        width: 100%;
        border-right: none;
        border-bottom: 1px solid var(--border);
    }
    
    .main-header {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .search-wrapper {
        width: 100%;
    }
    
    .conversations-list {
        padding: 1rem;
    }
}

@media (max-width: 480px) {
    .conversation-card {
        padding: 1rem;
    }
    
    .avatar-icon {
        width: 40px;
        height: 40px;
        font-size: 1.2rem;
    }
    
    .conversation-subject {
        font-size: 0.9rem;
    }
    
    .report-badge {
        display: none;
    }
    
    .meta-badges {
        flex-direction: column;
        gap: 0.25rem;
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // ===== FILE UPLOAD PREVIEW =====
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                const file = this.files[0];
                filePreview.innerHTML = `
                    <i class="bi bi-paperclip"></i>
                    <span>${file.name} (${(file.size / 1024).toFixed(1)} KB)</span>
                `;
                filePreview.classList.add('active');
                
                // Update upload label
                document.getElementById('fileUploadLabel').innerHTML = `
                    <i class="bi bi-check-circle-fill" style="color: var(--success);"></i>
                    File attached
                    ${fileInput.outerHTML}
                `;
            } else {
                filePreview.classList.remove('active');
                document.getElementById('fileUploadLabel').innerHTML = `
                    <i class="bi bi-paperclip"></i>
                    Attach File
                    ${fileInput.outerHTML}
                `;
            }
        });
    }
    
    // ===== SEARCH CONVERSATIONS =====
    const searchInput = document.getElementById('searchConversations');
    const conversationCards = document.querySelectorAll('.conversation-card');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            
            conversationCards.forEach(card => {
                const searchText = card.dataset.searchText?.toLowerCase() || '';
                const subject = card.querySelector('.conversation-subject')?.textContent.toLowerCase() || '';
                const messages = card.querySelector('.preview-text')?.textContent.toLowerCase() || '';
                
                const matches = subject.includes(query) || messages.includes(query) || searchText.includes(query);
                card.style.display = matches ? 'flex' : 'none';
            });
        });
    }
    
    // ===== ANIMATED ENTRY =====
    conversationCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });
});
</script>
{% endblock %}