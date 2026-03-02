<!-- customer/chat_room.html -->
{% extends 'customer/base.html' %}
{% load static %}
{% load chat_extras %}

{% block content %}
<div class="chat-fullscreen">
    <!-- Chat Sidebar - Conversations (optional) -->
    <div class="chat-sidebar">
        <div class="sidebar-header">
            <div class="header-top">
                <h2 class="sidebar-title">Conversations</h2>
                <span class="header-badge" id="sidebarUnread">3</span>
            </div>
            <div class="sidebar-search">
                <i class="bi bi-search"></i>
                <input type="text" placeholder="Search conversations..." class="search-input">
            </div>
        </div>
        
        <div class="conversations-list">
            <!-- This would be populated with other conversations -->
            <a href="#" class="conversation-item active">
                <div class="conversation-avatar">
                    {% if conversation.store.store_logo %}
                    <img src="{{ conversation.store.store_logo.url }}" alt="{{ conversation.store.store_name }}">
                    {% else %}
                    <div class="avatar-placeholder" style="background: linear-gradient(135deg, var(--primary), var(--primary-dark));">
                        {{ conversation.store.store_name|first|upper }}
                    </div>
                    {% endif %}
                </div>
                <div class="conversation-info">
                    <div class="conv-header">
                        <span class="conv-name">{{ conversation.store.store_name }}</span>
                        <span class="conv-time">now</span>
                    </div>
                    <div class="conv-preview">
                        <span class="preview-text">{{ messages.last.content|truncatechars:30 }}</span>
                        <span class="unread-badge">2</span>
                    </div>
                </div>
            </a>
        </div>
    </div>

    <!-- Main Chat Area -->
    <div class="chat-main">
        <!-- Chat Header -->
        <div class="chat-header">
            <div class="header-left">
                <a href="{% url 'customer_chat_list' %}" class="back-button">
                    <i class="bi bi-arrow-left"></i>
                </a>
                
                <div class="chat-avatar-wrapper">
                    <div class="chat-avatar">
                        {% if conversation.store.store_logo %}
                        <img src="{{ conversation.store.store_logo.url }}" alt="{{ conversation.store.store_name }}">
                        {% else %}
                        <div class="avatar-placeholder" style="background: linear-gradient(135deg, var(--primary), var(--primary-dark));">
                            {{ conversation.store.store_name|first|upper }}
                        </div>
                        {% endif %}
                    </div>
                    <span class="status-indicator online" title="Online"></span>
                </div>
                
                <div class="chat-info">
                    <h3 class="chat-name">{{ conversation.store.store_name }}</h3>
                    <div class="chat-meta">
                        <span class="chat-status online">● Online</span>
                        {% if conversation.book %}
                        <span class="chat-book">
                            <i class="bi bi-book"></i> {{ conversation.book.title|truncatechars:30 }}
                        </span>
                        {% endif %}
                    </div>
                </div>
            </div>
            
            <div class="header-right">
                <button class="header-icon-btn" id="searchMessagesBtn">
                    <i class="bi bi-search"></i>
                </button>
                <button class="header-icon-btn" id="moreOptionsBtn">
                    <i class="bi bi-three-dots-vertical"></i>
                </button>
            </div>
        </div>

        <!-- Messages Area -->
        <div class="messages-area" id="messageArea">
            <!-- Date Separator -->
            <div class="date-separator">
                <span class="date-badge">Today</span>
            </div>
            
            <div class="messages-container" id="messagesContainer">
                {% for message in messages %}
                <div class="message-wrapper {% if message.sender == request.user %}message-out{% else %}message-in{% endif %}" 
                     data-message-id="{{ message.id }}"
                     data-timestamp="{{ message.timestamp|date:'c' }}">
                    
                    <!-- Avatar for incoming messages -->
                    {% if message.sender != request.user %}
                    <div class="message-avatar">
                        {% if conversation.store.store_logo %}
                        <img src="{{ conversation.store.store_logo.url }}" alt="">
                        {% else %}
                        <div class="avatar-placeholder small" style="background: linear-gradient(135deg, var(--primary), var(--primary-dark));">
                            {{ conversation.store.store_name|first|upper }}
                        </div>
                        {% endif %}
                    </div>
                    {% endif %}
                    
                    <div class="message-content-wrapper">
                        <div class="message-bubble">
                            <div class="message-text">{{ message.content|linebreaksbr }}</div>
                            
                            {% if message.attachment %}
                            <div class="message-attachment">
                                <i class="bi bi-paperclip"></i>
                                <span>Attachment</span>
                            </div>
                            {% endif %}
                            
                            <div class="message-footer">
                                <span class="message-time">{{ message.timestamp|date:"H:i" }}</span>
                                
                                {% if message.sender == request.user %}
                                <div class="message-status">
                                    {% if message.is_read %}
                                    <i class="bi bi-check2-all read" title="Read"></i>
                                    {% else %}
                                    <i class="bi bi-check2" title="Sent"></i>
                                    {% endif %}
                                </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                {% empty %}
                <div class="empty-state">
                    <div class="empty-state-icon">
                        <i class="bi bi-chat-dots"></i>
                    </div>
                    <h3 class="empty-state-title">No messages yet</h3>
                    <p class="empty-state-text">Start a conversation with {{ conversation.store.store_name }}</p>
                </div>
                {% endfor %}
            </div>
            
            <!-- Scroll to bottom button (appears when scrolled up) -->
            <button class="scroll-bottom-btn" id="scrollBottomBtn" style="display: none;">
                <i class="bi bi-arrow-down"></i>
                <span class="unread-indicator" id="unreadIndicator">0</span>
            </button>
        </div>

        <!-- Message Input Area -->
        <div class="input-area">
            <form id="messageForm" class="message-form">
                {% csrf_token %}
                
                <div class="input-actions">
                    <button type="button" class="input-action-btn" id="attachBtn">
                        <i class="bi bi-paperclip"></i>
                    </button>
                    <button type="button" class="input-action-btn" id="emojiBtn">
                        <i class="bi bi-emoji-smile"></i>
                    </button>
                </div>
                
                <div class="input-wrapper">
                    <textarea 
                        id="messageInput" 
                        class="message-input" 
                        placeholder="Type a message..." 
                        autocomplete="off"
                        autofocus
                        rows="1"></textarea>
                    
                    <div class="input-tools">
                        <button type="button" class="input-tool-btn" id="voiceBtn">
                            <i class="bi bi-mic"></i>
                        </button>
                    </div>
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
                <span class="typing-text">{{ conversation.store.store_name }} is typing...</span>
            </div>
        </div>
    </div>

    <!-- Info Sidebar (optional) -->
    <div class="info-sidebar" id="infoSidebar" style="display: none;">
        <div class="info-header">
            <h3>Chat Info</h3>
            <button class="close-info-btn" id="closeInfoBtn">
                <i class="bi bi-x-lg"></i>
            </button>
        </div>
        
        <div class="info-content">
            <div class="store-profile">
                <div class="store-avatar-large">
                    {% if conversation.store.store_logo %}
                    <img src="{{ conversation.store.store_logo.url }}" alt="">
                    {% else %}
                    <div class="avatar-placeholder large" style="background: linear-gradient(135deg, var(--primary), var(--primary-dark));">
                        {{ conversation.store.store_name|first|upper }}
                    </div>
                    {% endif %}
                </div>
                <h4>{{ conversation.store.store_name }}</h4>
                <p class="store-status">Active now</p>
                
                <div class="store-actions">
                    <button class="store-action-btn">
                        <i class="bi bi-shop"></i>
                        View Store
                    </button>
                    {% if conversation.book %}
                    <button class="store-action-btn">
                        <i class="bi bi-book"></i>
                        View Book
                    </button>
                    {% endif %}
                </div>
            </div>
            
            <div class="info-section">
                <h5>About Store</h5>
                <p>{{ conversation.store.store_description|truncatechars:100 }}</p>
            </div>
            
            <div class="info-section">
                <h5>Media & Files</h5>
                <div class="media-grid">
                    <div class="media-placeholder">
                        <i class="bi bi-image"></i>
                        <span>No media</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Message Context Menu (Hidden by default) -->
<div class="context-menu" id="contextMenu" style="display: none;">
    <button class="context-menu-item">
        <i class="bi bi-clipboard"></i> Copy
    </button>
    <button class="context-menu-item">
        <i class="bi bi-trash"></i> Delete
    </button>
    <button class="context-menu-item">
        <i class="bi bi-info-circle"></i> Info
    </button>
</div>

<style>
/* ===== FULLSCREEN CHAT LAYOUT ===== */
.chat-fullscreen {
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
.chat-sidebar {
    width: 320px;
    background: var(--bg-card);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.sidebar-header {
    padding: 1.5rem 1.5rem 1rem;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
}

.header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.sidebar-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.02em;
}

.header-badge {
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(8px);
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.3);
}

.sidebar-search {
    display: flex;
    align-items: center;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    border: 1.5px solid rgba(255,255,255,0.2);
    border-radius: 999px;
    padding: 0.5rem 1rem;
    transition: all var(--t-fast);
}

.sidebar-search i {
    color: rgba(255,255,255,0.7);
    font-size: 0.9rem;
    margin-right: 0.5rem;
}

.sidebar-search input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 0.85rem;
}

.sidebar-search input::placeholder {
    color: rgba(255,255,255,0.5);
}

.conversations-list {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
}

.conversation-item {
    display: flex;
    padding: 0.75rem;
    border-radius: var(--radius);
    text-decoration: none;
    color: var(--text-primary);
    transition: all var(--t-fast);
    margin-bottom: 0.25rem;
}

.conversation-item:hover {
    background: var(--primary-soft);
}

.conversation-item.active {
    background: var(--primary-soft);
    border-left: 3px solid var(--primary);
}

.conversation-avatar {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    overflow: hidden;
    margin-right: 0.75rem;
    flex-shrink: 0;
}

.conversation-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.conversation-info {
    flex: 1;
    min-width: 0;
}

.conv-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.25rem;
}

.conv-name {
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-primary);
}

.conv-time {
    font-size: 0.7rem;
    color: var(--text-muted);
}

.conv-preview {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.preview-text {
    font-size: 0.8rem;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 160px;
}

/* ===== MAIN CHAT AREA ===== */
.chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: var(--bg-card);
    position: relative;
}

/* Chat Header */
.chat-header {
    padding: 1rem 1.5rem;
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

.back-button {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    text-decoration: none;
    transition: all var(--t-fast);
}

.back-button:hover {
    background: var(--primary-soft);
    color: var(--primary);
    border-color: var(--primary);
}

.chat-avatar-wrapper {
    position: relative;
    width: 44px;
    height: 44px;
}

.chat-avatar {
    width: 44px;
    height: 44px;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.chat-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 1.2rem;
}

.avatar-placeholder.small {
    font-size: 0.9rem;
}

.avatar-placeholder.large {
    font-size: 2rem;
}

.status-indicator {
    position: absolute;
    bottom: 2px;
    right: 2px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--success);
    border: 2px solid var(--bg-card);
}

.status-indicator.online {
    background: var(--success);
    box-shadow: 0 0 0 2px rgba(0,201,139,0.2);
}

.chat-info {
    flex: 1;
    min-width: 0;
}

.chat-name {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.1rem;
}

.chat-meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.75rem;
}

.chat-status {
    color: var(--success);
    font-weight: 600;
}

.chat-status.online {
    color: var(--success);
}

.chat-book {
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 0.2rem;
}

.chat-book i {
    font-size: 0.7rem;
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
    padding: 2rem 1.5rem;
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

/* Messages Container */
.messages-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 800px;
    margin: 0 auto;
}

/* Message Wrapper */
.message-wrapper {
    display: flex;
    gap: 0.75rem;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message-in {
    justify-content: flex-start;
}

.message-out {
    justify-content: flex-end;
}

/* Message Avatar */
.message-avatar {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    overflow: hidden;
    flex-shrink: 0;
    align-self: flex-end;
    margin-bottom: 0.5rem;
}

.message-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.message-out .message-avatar {
    display: none;
}

/* Message Content */
.message-content-wrapper {
    max-width: 65%;
    min-width: 120px;
}

.message-bubble {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 0.75rem 1rem;
    box-shadow: var(--shadow-sm);
    transition: all var(--t-fast);
}

.message-out .message-bubble {
    background: var(--primary);
    border-color: var(--primary);
    color: white;
    border-bottom-right-radius: 0;
}

.message-in .message-bubble {
    border-bottom-left-radius: 0;
}

.message-text {
    font-size: 0.9rem;
    line-height: 1.5;
    word-wrap: break-word;
    margin-bottom: 0.5rem;
}

.message-out .message-text {
    color: white;
}

.message-attachment {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    background: rgba(0,0,0,0.05);
    border-radius: var(--radius-sm);
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
}

.message-out .message-attachment {
    background: rgba(255,255,255,0.15);
}

.message-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem;
    font-size: 0.7rem;
}

.message-out .message-footer {
    color: rgba(255,255,255,0.8);
}

.message-in .message-footer {
    color: var(--text-muted);
}

.message-time {
    opacity: 0.8;
}

.message-status i {
    font-size: 0.9rem;
}

.message-status .read {
    color: #4fc3f7;
}

/* Scroll to bottom button */
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

.unread-indicator {
    position: absolute;
    top: -4px;
    right: -4px;
    background: var(--danger);
    color: white;
    font-size: 0.6rem;
    font-weight: 700;
    min-width: 16px;
    height: 16px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 4px;
}

/* Input Area */
.input-area {
    padding: 1rem 1.5rem;
    background: var(--bg-card);
    border-top: 1px solid var(--border);
    position: relative;
}

.message-form {
    display: flex;
    align-items: flex-end;
    gap: 0.75rem;
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
    flex: 1;
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
    flex-shrink: 0;
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
    width: 280px;
    background: var(--bg-card);
    border-left: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    animation: slideInRight 0.3s ease;
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
    padding: 1.5rem 1.5rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
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

.store-profile {
    text-align: center;
    margin-bottom: 2rem;
}

.store-avatar-large {
    width: 80px;
    height: 80px;
    border-radius: 20px;
    overflow: hidden;
    margin: 0 auto 1rem;
    box-shadow: var(--shadow);
}

.store-avatar-large img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.store-profile h4 {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}

.store-status {
    font-size: 0.8rem;
    color: var(--success);
    margin-bottom: 1rem;
}

.store-actions {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
}

.store-action-btn {
    padding: 0.5rem 1rem;
    border-radius: 999px;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    font-size: 0.75rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    cursor: pointer;
    transition: all var(--t-fast);
}

.store-action-btn:hover {
    background: var(--primary-soft);
    color: var(--primary);
    border-color: var(--primary);
}

.info-section {
    margin-bottom: 1.5rem;
}

.info-section h5 {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.info-section p {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

.media-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
}

.media-placeholder {
    aspect-ratio: 1;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 0.7rem;
}

.media-placeholder i {
    font-size: 1rem;
    margin-bottom: 0.25rem;
}

/* Context Menu */
.context-menu {
    position: absolute;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    padding: 0.5rem;
    z-index: 1000;
    min-width: 150px;
}

.context-menu-item {
    width: 100%;
    padding: 0.5rem 1rem;
    background: transparent;
    border: none;
    color: var(--text-secondary);
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    border-radius: var(--radius-sm);
    transition: all var(--t-fast);
}

.context-menu-item:hover {
    background: var(--primary-soft);
    color: var(--primary);
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
}

.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.3;
}

.empty-state-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.empty-state-text {
    font-size: 0.9rem;
    color: var(--text-secondary);
}

/* Responsive */
@media (max-width: 1024px) {
    .chat-sidebar {
        width: 280px;
    }
    
    .message-content-wrapper {
        max-width: 75%;
    }
}

@media (max-width: 768px) {
    .chat-fullscreen {
        flex-direction: column;
        height: auto;
        min-height: calc(100vh - var(--header-h) - 2rem);
    }
    
    .chat-sidebar {
        width: 100%;
        border-right: none;
        border-bottom: 1px solid var(--border);
    }
    
    .info-sidebar {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        z-index: 100;
        box-shadow: var(--shadow-xl);
    }
    
    .message-content-wrapper {
        max-width: 85%;
    }
    
    .header-right {
        gap: 0.25rem;
    }
    
    .input-area {
        padding: 0.75rem 1rem;
    }
}

@media (max-width: 480px) {
    .chat-header {
        padding: 0.75rem 1rem;
    }
    
    .chat-avatar-wrapper {
        width: 36px;
        height: 36px;
    }
    
    .chat-avatar {
        width: 36px;
        height: 36px;
    }
    
    .chat-name {
        font-size: 0.9rem;
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

<script>
document.addEventListener('DOMContentLoaded', function() {
    // ===== ELEMENTS =====
    const messageArea = document.getElementById('messageArea');
    const messagesContainer = document.getElementById('messagesContainer');
    const messageForm = document.getElementById('messageForm');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const scrollBottomBtn = document.getElementById('scrollBottomBtn');
    const unreadIndicator = document.getElementById('unreadIndicator');
    const typingIndicator = document.getElementById('typingIndicator');
    const infoSidebar = document.getElementById('infoSidebar');
    const moreOptionsBtn = document.getElementById('moreOptionsBtn');
    const closeInfoBtn = document.getElementById('closeInfoBtn');
    const contextMenu = document.getElementById('contextMenu');
    
    const conversationId = {{ conversation.id }};
    let lastMessageCount = {{ messages|length }};
    let isAtBottom = true;
    let unreadCount = 0;
    
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
        
        if (isAtBottom) {
            scrollBottomBtn.style.display = 'none';
            unreadCount = 0;
            if (unreadIndicator) unreadIndicator.textContent = '0';
        } else {
            scrollBottomBtn.style.display = 'flex';
        }
    }
    
    // Scroll to bottom on load
    scrollToBottom();
    
    // Check scroll position on scroll
    messageArea.addEventListener('scroll', checkIfAtBottom);
    
    // Scroll bottom button click
    scrollBottomBtn.addEventListener('click', () => {
        scrollToBottom(true);
    });
    
    // ===== MESSAGE INPUT =====
    // Auto-resize textarea
    function autoResize() {
        messageInput.style.height = 'auto';
        messageInput.style.height = Math.min(messageInput.scrollHeight, 100) + 'px';
    }
    
    messageInput.addEventListener('input', function() {
        autoResize();
        sendBtn.disabled = !this.value.trim();
    });
    
    // Enable/disable send button
    messageInput.addEventListener('input', function() {
        sendBtn.disabled = !this.value.trim();
    });
    
    // Handle Enter key (send on Enter, Shift+Enter for new line)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (this.value.trim()) {
                messageForm.dispatchEvent(new Event('submit'));
            }
        }
    });
    
    // ===== SEND MESSAGE =====
    messageForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const content = messageInput.value.trim();
        if (!content) return;
        
        // Store current value and clear input
        const messageText = content;
        messageInput.value = '';
        messageInput.style.height = 'auto';
        sendBtn.disabled = true;
        
        // Show sending state
        sendBtn.innerHTML = '<i class="bi bi-hourglass-split"></i>';
        
        try {
            const response = await fetch(`/chat/${conversationId}/send/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ content: messageText })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Instead of reloading, append the message dynamically
                appendNewMessage(messageText, data.message);
                scrollToBottom(true);
            } else {
                alert('Error sending message: ' + data.error);
                messageInput.value = messageText;
                sendBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to send message');
            messageInput.value = messageText;
            sendBtn.disabled = false;
        } finally {
            sendBtn.innerHTML = '<i class="bi bi-send-fill"></i>';
            messageInput.focus();
        }
    });
    
    function appendNewMessage(content, messageData) {
        const time = new Date().toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: false 
        });
        
        const messageHtml = `
            <div class="message-wrapper message-out" data-message-id="new">
                <div class="message-content-wrapper">
                    <div class="message-bubble">
                        <div class="message-text">${content.replace(/\n/g, '<br>')}</div>
                        <div class="message-footer">
                            <span class="message-time">${time}</span>
                            <div class="message-status">
                                <i class="bi bi-check2" title="Sent"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.insertAdjacentHTML('beforeend', messageHtml);
    }
    
    // ===== POLLING FOR NEW MESSAGES =====
    setInterval(async () => {
        try {
            const response = await fetch(window.location.href, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (response.ok) {
                const currentMessages = document.querySelectorAll('.message-wrapper').length;
                if (currentMessages !== lastMessageCount) {
                    // New message received
                    if (isAtBottom) {
                        location.reload();
                    } else {
                        unreadCount++;
                        if (unreadIndicator) unreadIndicator.textContent = unreadCount;
                        scrollBottomBtn.style.display = 'flex';
                        
                        // Show notification dot in header
                        const headerUnread = document.querySelector('.header-badge');
                        if (headerUnread) {
                            headerUnread.textContent = unreadCount;
                            headerUnread.style.display = 'inline-block';
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 3000);
    
    // ===== TYPING INDICATOR =====
    let typingTimeout;
    messageInput.addEventListener('keypress', function() {
        // Show typing indicator (simplified)
        typingIndicator.style.display = 'flex';
        
        clearTimeout(typingTimeout);
        typingTimeout = setTimeout(() => {
            typingIndicator.style.display = 'none';
        }, 2000);
    });
    
    // ===== MARK MESSAGES AS READ =====
    fetch(`/chat/${conversationId}/mark-read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    });
    
    // ===== INFO SIDEBAR TOGGLE =====
    if (moreOptionsBtn) {
        moreOptionsBtn.addEventListener('click', function() {
            if (infoSidebar.style.display === 'none') {
                infoSidebar.style.display = 'flex';
            } else {
                infoSidebar.style.display = 'none';
            }
        });
    }
    
    if (closeInfoBtn) {
        closeInfoBtn.addEventListener('click', function() {
            infoSidebar.style.display = 'none';
        });
    }
    
    // ===== ATTACHMENT BUTTON =====
    document.getElementById('attachBtn').addEventListener('click', function() {
        // Create a file input dynamically
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*,.pdf,.doc,.docx,.txt';
        fileInput.click();
        
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                alert('File upload would be handled here. Selected: ' + this.files[0].name);
            }
        });
    });
    
    // ===== EMOJI BUTTON (placeholder) =====
    document.getElementById('emojiBtn').addEventListener('click', function() {
        alert('Emoji picker would open here');
    });
    
    // ===== VOICE BUTTON (placeholder) =====
    document.getElementById('voiceBtn').addEventListener('click', function() {
        alert('Voice recording would start here');
    });
    
    // ===== CONTEXT MENU FOR MESSAGES =====
    document.querySelectorAll('.message-wrapper').forEach(msg => {
        msg.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            
            contextMenu.style.display = 'block';
            contextMenu.style.left = e.pageX + 'px';
            contextMenu.style.top = e.pageY + 'px';
            
            // Hide menu after clicking
            setTimeout(() => {
                document.addEventListener('click', function hideMenu() {
                    contextMenu.style.display = 'none';
                    document.removeEventListener('click', hideMenu);
                }, { once: true });
            }, 100);
        });
    });
    
    // ===== SEARCH MESSAGES (placeholder) =====
    document.getElementById('searchMessagesBtn').addEventListener('click', function() {
        alert('Search in conversation would open here');
    });
    
    // ===== FOCUS INPUT ON LOAD =====
    messageInput.focus();
});
</script>
{% endblock %}