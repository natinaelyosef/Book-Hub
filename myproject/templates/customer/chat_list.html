<!-- customer/chat_list.html -->
{% extends 'customer/base.html' %}
{% load chat_extras %}

{% block content %}
<div class="chat-fullscreen">
    <!-- Sidebar - Conversations List -->
    <div class="chat-sidebar">
        <!-- Sidebar Header -->
        <div class="sidebar-header">
            <div class="header-top">
                <h1 class="header-title">Messages</h1>
                <span class="header-badge" id="totalUnreadBadge">0</span>
            </div>
            
            <!-- Search -->
            <div class="search-wrapper">
                <div class="search-box">
                    <i class="bi bi-search search-icon"></i>
                    <input type="text" 
                           class="search-input" 
                           placeholder="Search conversations..." 
                           id="chat-search"
                           value="{{ search_query }}">
                    <button class="search-clear" id="clearSearch" style="display: none;">
                        <i class="bi bi-x-lg"></i>
                    </button>
                </div>
            </div>
            
            <!-- Filter Tabs -->
            <div class="filter-tabs">
                <button class="filter-tab active" data-filter="all">
                    <i class="bi bi-chat-dots"></i>
                    All
                </button>
                <button class="filter-tab" data-filter="unread">
                    <i class="bi bi-envelope-paper"></i>
                    Unread
                    <span class="filter-badge" id="unreadFilterBadge">0</span>
                </button>
                <button class="filter-tab" data-filter="stores">
                    <i class="bi bi-shop"></i>
                    Stores
                </button>
                <button class="filter-tab" data-filter="books">
                    <i class="bi bi-book"></i>
                    Books
                </button>
            </div>
        </div>
        
        <!-- Conversations List -->
        <div class="conversations-list">
            {% for item in conversation_data %}
            <a href="{% url 'chat_room' item.conversation.id %}" 
               class="conversation-item {% if item.unread_count %}unread{% endif %}"
               data-conversation-id="{{ item.conversation.id }}"
               data-last-message="{% if item.last_message %}{{ item.last_message.content }}{% endif %}"
               data-store="{{ item.conversation.store.store_name }}"
               data-book="{% if item.conversation.book %}{{ item.conversation.book.title }}{% endif %}">
                
                <!-- Avatar -->
                <div class="conversation-avatar">
                    {% if item.conversation.store.store_logo %}
                    <img src="{{ item.conversation.store.store_logo.url }}" alt="{{ item.conversation.store.store_name }}">
                    {% else %}
                    <div class="avatar-placeholder" style="background: linear-gradient(135deg, var(--primary), var(--primary-dark));">
                        {{ item.conversation.store.store_name|first|upper }}
                    </div>
                    {% endif %}
                    <span class="status-indicator" title="Online" style="display: none;"></span>
                </div>
                
                <!-- Conversation Info -->
                <div class="conversation-info">
                    <div class="info-header">
                        <span class="conversation-name">{{ item.conversation.store.store_name }}</span>
                        <span class="conversation-time">
                            {% if item.last_message %}
                                {{ item.last_message.timestamp|timesince|cut:","|truncatechars:8 }}
                            {% else %}
                                {{ item.conversation.updated_at|timesince|cut:","|truncatechars:8 }}
                            {% endif %}
                        </span>
                    </div>
                    
                    <div class="info-preview">
                        <div class="preview-wrapper">
                            {% if item.last_message %}
                                {% if item.last_message.sender == request.user %}
                                <span class="preview-sender">You: </span>
                                {% endif %}
                                <span class="preview-text {% if not item.last_message.content %}empty-message{% endif %}">
                                    {% if item.last_message.content %}
                                        {{ item.last_message.content|truncatechars:45 }}
                                    {% else %}
                                        <span class="attachment-indicator">
                                            <i class="bi bi-paperclip"></i> Attachment
                                        </span>
                                    {% endif %}
                                </span>
                            {% else %}
                                <span class="preview-text empty-message">
                                    <i class="bi bi-chat"></i> No messages yet
                                </span>
                            {% endif %}
                        </div>
                        
                        <div class="preview-meta">
                            {% if item.conversation.book %}
                            <span class="book-badge">
                                <i class="bi bi-book"></i>
                                {{ item.conversation.book.title|truncatechars:15 }}
                            </span>
                            {% endif %}
                            
                            {% if item.unread_count %}
                            <span class="unread-badge pulse">{{ item.unread_count }}</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </a>
            {% empty %}
            <div class="empty-conversations">
                <div class="empty-icon">
                    <i class="bi bi-chat-dots"></i>
                </div>
                <h3>No conversations yet</h3>
                <p>Start chatting with store owners about your favorite books</p>
                <div class="empty-actions">
                    <a href="{% url 'customer_dashboard' %}" class="btn btn-primary">
                        <i class="bi bi-book"></i>
                        Browse Books
                    </a>
                    <a href="{% url 'store_list' %}" class="btn btn-outline">
                        <i class="bi bi-shop"></i>
                        View Stores
                    </a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <!-- Main Content Area - Welcome Screen -->
    <div class="chat-main">
        <div class="welcome-screen">
            <div class="welcome-icon">
                <i class="bi bi-chat-dots"></i>
            </div>
            <h2 class="welcome-title">Your Messages</h2>
            <p class="welcome-text">Select a conversation from the sidebar to start chatting</p>
            
            <div class="welcome-features">
                <div class="feature-item">
                    <div class="feature-icon">
                        <i class="bi bi-shop"></i>
                    </div>
                    <div class="feature-text">
                        <h4>Chat with Stores</h4>
                        <p>Ask questions about books, availability, and more</p>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">
                        <i class="bi bi-book"></i>
                    </div>
                    <div class="feature-text">
                        <h4>Discuss Books</h4>
                        <p>Get recommendations and discuss your favorite reads</p>
                    </div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">
                        <i class="bi bi-clock-history"></i>
                    </div>
                    <div class="feature-text">
                        <h4>Track Orders</h4>
                        <p>Get real-time updates about your orders</p>
                    </div>
                </div>
            </div>
            
           
        </div>
    </div>
</div>

<!-- New Chat Modal -->
<div class="modal" id="newChatModal">
    <div class="modal-overlay"></div>
    <div class="modal-container">
        <div class="modal-header">
            <h3 class="modal-title">Start New Conversation</h3>
            <button class="modal-close"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="modal-body">
            <div class="modal-search">
                <i class="bi bi-search"></i>
                <input type="text" placeholder="Search stores or books..." id="modalSearch">
            </div>
            
            <div class="quick-actions">
                <h4>Quick Start</h4>
                <div class="quick-buttons">
                    <a href="{% url 'store_list' %}" class="quick-btn">
                        <i class="bi bi-shop"></i>
                        Browse Stores
                    </a>
                    <a href="{% url 'customer_dashboard' %}" class="quick-btn">
                        <i class="bi bi-book"></i>
                        Browse Books
                    </a>
                </div>
            </div>
            
            <div class="recent-stores">
                <h4>Recent Stores</h4>
                <div class="stores-list" id="storesList">
                    <!-- Will be populated via AJAX -->
                    <div class="loading-spinner">
                        <i class="bi bi-arrow-repeat spin"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
/* ===== FULLSCREEN LAYOUT ===== */
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
    width: 380px;
    background: var(--bg-card);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

/* Sidebar Header */
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

.header-title {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
}

.header-badge {
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(8px);
    padding: 0.2rem 0.8rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.3);
}

/* Search */
.search-wrapper {
    margin-bottom: 1rem;
}

.search-box {
    display: flex;
    align-items: center;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    border: 1.5px solid rgba(255,255,255,0.2);
    border-radius: 999px;
    padding: 0.3rem 0.3rem 0.3rem 1rem;
    transition: all var(--t-fast);
}

.search-box:focus-within {
    background: rgba(255,255,255,0.2);
    border-color: rgba(255,255,255,0.4);
    box-shadow: 0 0 0 4px rgba(255,255,255,0.1);
}

.search-icon {
    color: rgba(255,255,255,0.7);
    font-size: 0.9rem;
    margin-right: 0.5rem;
}

.search-input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 0.9rem;
    padding: 0.6rem 0;
}

.search-input::placeholder {
    color: rgba(255,255,255,0.5);
}

.search-clear {
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all var(--t-fast);
    margin-right: 0.3rem;
}

.search-clear:hover {
    background: rgba(255,255,255,0.3);
    transform: scale(1.1);
}

/* Filter Tabs */
.filter-tabs {
    display: flex;
    gap: 0.5rem;
    overflow-x: auto;
    padding-bottom: 0.25rem;
    scrollbar-width: thin;
}

.filter-tabs::-webkit-scrollbar {
    height: 3px;
}

.filter-tabs::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.3);
    border-radius: 10px;
}

.filter-tab {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.9);
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--t-fast);
    white-space: nowrap;
    position: relative;
}

.filter-tab i {
    font-size: 0.8rem;
}

.filter-tab:hover {
    background: rgba(255,255,255,0.25);
}

.filter-tab.active {
    background: white;
    color: var(--primary);
    border-color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.filter-badge {
    background: var(--danger);
    color: white;
    font-size: 0.65rem;
    padding: 0.1rem 0.4rem;
    border-radius: 999px;
    margin-left: 0.3rem;
}

/* Conversations List */
.conversations-list {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
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
    background-color: var(--border);
    border-radius: 20px;
}

/* Conversation Item */
.conversation-item {
    display: flex;
    padding: 1rem;
    margin-bottom: 0.5rem;
    border-radius: var(--radius-lg);
    background: var(--bg-card);
    border: 1px solid var(--border);
    text-decoration: none;
    color: var(--text-primary);
    transition: all var(--t-fast);
    animation: slideIn 0.3s ease;
    position: relative;
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

.conversation-item:hover {
    transform: translateX(4px);
    border-color: var(--primary);
    box-shadow: var(--shadow);
}

.conversation-item.unread {
    background: var(--primary-soft);
    border-left: 3px solid var(--primary);
}

/* Avatar */
.conversation-avatar {
    position: relative;
    width: 48px;
    height: 48px;
    border-radius: 14px;
    overflow: hidden;
    margin-right: 1rem;
    flex-shrink: 0;
    box-shadow: var(--shadow-sm);
}

.conversation-avatar img {
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

/* Conversation Info */
.conversation-info {
    flex: 1;
    min-width: 0;
}

.info-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.3rem;
}

.conversation-name {
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--text-primary);
}

.conversation-time {
    font-size: 0.7rem;
    color: var(--text-muted);
}

.info-preview {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
}

.preview-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    min-width: 0;
}

.preview-sender {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--primary);
    white-space: nowrap;
}

.preview-text {
    font-size: 0.8rem;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.preview-text.empty-message {
    color: var(--text-muted);
    font-style: italic;
}

.attachment-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.2rem;
    color: var(--primary);
}

.attachment-indicator i {
    font-size: 0.7rem;
}

.preview-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-shrink: 0;
}

.book-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.2rem;
    padding: 0.2rem 0.6rem;
    background: var(--accent-soft);
    border-radius: 999px;
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--accent);
    border: 1px solid rgba(245,176,66,0.2);
    white-space: nowrap;
}

.book-badge i {
    font-size: 0.6rem;
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

.pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
}

/* ===== MAIN CONTENT AREA ===== */
.chat-main {
    flex: 1;
    background: var(--bg-card);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.welcome-screen {
    max-width: 500px;
    text-align: center;
}

.welcome-icon {
    font-size: 4rem;
    color: var(--primary);
    margin-bottom: 1.5rem;
    opacity: 0.5;
}

.welcome-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}

.welcome-text {
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin-bottom: 2.5rem;
}

.welcome-features {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-bottom: 2.5rem;
}

.feature-item {
    text-align: center;
}

.feature-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: var(--primary-soft);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    color: var(--primary);
    font-size: 1.2rem;
    transition: all var(--t);
}

.feature-item:hover .feature-icon {
    background: var(--primary);
    color: white;
    transform: translateY(-4px);
}

.feature-text h4 {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.3rem;
}

.feature-text p {
    font-size: 0.75rem;
    color: var(--text-muted);
    line-height: 1.4;
}

.new-chat-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.8rem 2rem;
    border-radius: 999px;
    background: var(--primary);
    color: white;
    border: none;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    transition: all var(--t-fast);
    box-shadow: 0 8px 20px var(--primary-glow);
}

.new-chat-btn:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 12px 28px var(--primary-glow);
}

/* ===== EMPTY STATE ===== */
.empty-conversations {
    text-align: center;
    padding: 3rem 1rem;
}

.empty-icon {
    font-size: 3rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
    opacity: 0.3;
}

.empty-conversations h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.empty-conversations p {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
}

.empty-actions {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
}

.btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.2rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    text-decoration: none;
    transition: all var(--t-fast);
    cursor: pointer;
    border: none;
}

.btn-primary {
    background: var(--primary);
    color: white;
    box-shadow: 0 4px 12px var(--primary-glow);
}

.btn-primary:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
}

.btn-outline {
    background: transparent;
    color: var(--text-secondary);
    border: 1.5px solid var(--border);
}

.btn-outline:hover {
    border-color: var(--primary);
    color: var(--primary);
    background: var(--primary-soft);
}

/* ===== MODAL ===== */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    display: none;
    align-items: center;
    justify-content: center;
}

.modal.active {
    display: flex;
}

.modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(8px);
    animation: fadeIn 0.2s ease;
}

.modal-container {
    position: relative;
    z-index: 1001;
    width: 90%;
    max-width: 500px;
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-xl);
    animation: slideUp 0.3s ease;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 1.5rem;
    border-bottom: 1px solid var(--border);
}

.modal-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
}

.modal-close {
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

.modal-close:hover {
    background: var(--danger-soft);
    color: var(--danger);
    border-color: var(--danger);
}

.modal-body {
    padding: 1.5rem;
}

.modal-search {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: var(--bg-raised);
    border: 1.5px solid var(--border);
    border-radius: 999px;
    margin-bottom: 1.5rem;
}

.modal-search i {
    color: var(--text-muted);
    font-size: 0.9rem;
}

.modal-search input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text-primary);
    font-size: 0.9rem;
}

.quick-actions {
    margin-bottom: 1.5rem;
}

.quick-actions h4 {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.quick-buttons {
    display: flex;
    gap: 0.5rem;
}

.quick-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.8rem;
    border-radius: var(--radius);
    background: var(--bg-raised);
    border: 1.5px solid var(--border);
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all var(--t-fast);
}

.quick-btn:hover {
    border-color: var(--primary);
    color: var(--primary);
    background: var(--primary-soft);
}

.recent-stores h4 {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stores-list {
    max-height: 200px;
    overflow-y: auto;
}

.loading-spinner {
    text-align: center;
    padding: 2rem;
    color: var(--text-muted);
}

.spin {
    animation: spin 1s linear infinite;
    font-size: 1.5rem;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1024px) {
    .chat-sidebar {
        width: 320px;
    }
    
    .welcome-features {
        gap: 1rem;
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
    
    .chat-main {
        display: none;
    }
    
    .conversation-item:hover {
        transform: none;
    }
    
    .welcome-features {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 480px) {
    .sidebar-header {
        padding: 1rem;
    }
    
    .conversations-list {
        padding: 0.5rem;
    }
    
    .conversation-item {
        padding: 0.8rem;
    }
    
    .conversation-avatar {
        width: 40px;
        height: 40px;
    }
    
    .book-badge {
        display: none;
    }
    
    .quick-buttons {
        flex-direction: column;
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // ===== SEARCH FUNCTIONALITY =====
    const searchInput = document.getElementById('chat-search');
    const clearBtn = document.getElementById('clearSearch');
    const conversationItems = document.querySelectorAll('.conversation-item');
    
    function performSearch() {
        const query = searchInput.value.toLowerCase().trim();
        
        // Show/hide clear button
        clearBtn.style.display = query ? 'flex' : 'none';
        
        conversationItems.forEach(item => {
            const chatName = item.dataset.store?.toLowerCase() || 
                            item.querySelector('.conversation-name').textContent.toLowerCase();
            const lastMessage = item.dataset.lastMessage?.toLowerCase() || '';
            const bookInfo = item.dataset.book?.toLowerCase() || '';
            
            const matches = chatName.includes(query) || 
                          lastMessage.includes(query) || 
                          bookInfo.includes(query);
            
            item.style.display = matches ? 'flex' : 'none';
        });
    }
    
    if (searchInput) {
        searchInput.addEventListener('input', performSearch);
    }
    
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            searchInput.value = '';
            performSearch();
            searchInput.focus();
        });
    }
    
    // ===== FILTER TABS =====
    const filterTabs = document.querySelectorAll('.filter-tab');
    const unreadBadge = document.getElementById('totalUnreadBadge');
    const unreadFilterBadge = document.getElementById('unreadFilterBadge');
    
    function updateUnreadCounts() {
        const unreadItems = document.querySelectorAll('.conversation-item.unread').length;
        if (unreadBadge) unreadBadge.textContent = unreadItems;
        if (unreadFilterBadge) {
            unreadFilterBadge.textContent = unreadItems;
            unreadFilterBadge.style.display = unreadItems > 0 ? 'inline-block' : 'none';
        }
    }
    
    filterTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            filterTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.dataset.filter;
            
            conversationItems.forEach(item => {
                const isUnread = item.classList.contains('unread');
                const hasBook = item.dataset.book;
                
                switch(filter) {
                    case 'all':
                        item.style.display = 'flex';
                        break;
                    case 'unread':
                        item.style.display = isUnread ? 'flex' : 'none';
                        break;
                    case 'stores':
                        item.style.display = 'flex';
                        break;
                    case 'books':
                        item.style.display = hasBook ? 'flex' : 'none';
                        break;
                }
            });
        });
    });
    
    // ===== NEW CHAT MODAL =====
    const newChatBtn = document.getElementById('newChatBtn');
    const modal = document.getElementById('newChatModal');
    const modalClose = document.querySelector('.modal-close');
    const modalOverlay = document.querySelector('.modal-overlay');
    
    function openModal() {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Simulate loading stores (replace with actual AJAX)
        setTimeout(() => {
            const storesList = document.getElementById('storesList');
            if (storesList) {
                storesList.innerHTML = `
                    <div class="empty-state" style="padding: 1rem;">
                        <p style="color: var(--text-muted);">Browse stores to start a conversation</p>
                    </div>
                `;
            }
        }, 500);
    }
    
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    if (newChatBtn) {
        newChatBtn.addEventListener('click', openModal);
    }
    
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }
    
    if (modalOverlay) {
        modalOverlay.addEventListener('click', closeModal);
    }
    
    // ===== INITIAL COUNTS =====
    updateUnreadCounts();
    
    // ===== ESCAPE KEY HANDLER =====
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
            closeModal();
        }
    });
    
    // ===== ANIMATED ENTRY =====
    conversationItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.03}s`;
    });
});
</script>
{% endblock %}