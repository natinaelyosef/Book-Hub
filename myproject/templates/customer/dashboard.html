{% extends 'customer/base.html' %}
{% load static %}
{% block title %}Browse Books · BookHub{% endblock %}

{% block extra_css %}
<style>
/* ══════════════════════════════════════════════════
   DASHBOARD — all tokens inherited from base.html
   ══════════════════════════════════════════════════ */

/* ── Results / info bar ── */
.results-bar {
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 0.75rem;
    padding: 1rem 1.25rem; margin-bottom: 2rem;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius-lg); box-shadow: var(--shadow-sm);
}
.results-text { font-size: 0.87rem; color: var(--text-secondary); font-weight: 500; }
.results-text strong { color: var(--text-primary); font-weight: 800; }
.results-text .hl { color: var(--primary); font-style: italic; }

/* Active filter pills */
.active-pills { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.65rem; }
.active-pill {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.22rem 0.7rem; border-radius: 999px;
    font-size: 0.7rem; font-weight: 700;
}
.pill-blue   { background: var(--primary-soft); color: var(--primary);  border: 1px solid var(--border); }
.pill-green  { background: var(--success-soft);  color: var(--success);  border: 1px solid rgba(0,201,139,0.2); }
.pill-purple { background: rgba(139,92,246,0.1);  color: #8B5CF6;        border: 1px solid rgba(139,92,246,0.2); }
.pill-close  { opacity: 0.6; cursor: pointer; transition: opacity var(--t-fast); text-decoration: none; color: inherit; }
.pill-close:hover { opacity: 1; color: inherit; }

/* ── Filter bar 2nd row (store + clear) ── */
.filter-row2 {
    display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;
    width: 100%; padding-top: 0.85rem; margin-top: 0.5rem;
    border-top: 1px solid var(--border-soft);
}
.filter-row2 label {
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: var(--text-muted); flex-shrink: 0;
    display: flex; align-items: center; gap: 0.4rem;
}
.filter-row2 label i { color: var(--primary); }

/* ── Empty state ── */
.empty-state {
    grid-column: 1 / -1;
    text-align: center; padding: 5rem 2rem;
}
.empty-icon {
    width: 80px; height: 80px; border-radius: var(--radius-lg);
    background: var(--primary-soft); border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; color: var(--primary); margin: 0 auto 1.5rem;
}
.empty-state h3 {
    font-size: 1.25rem; font-weight: 800; color: var(--text-primary);
    letter-spacing: -0.02em; margin-bottom: 0.5rem;
}
.empty-state p { font-size: 0.87rem; color: var(--text-muted); margin-bottom: 1.5rem; }

/* ── Genre badge on card ── */
.book-genre-tag {
    display: inline-flex; align-items: center;
    padding: 0.18rem 0.6rem; border-radius: 999px;
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.3px;
    background: var(--primary-soft); color: var(--primary);
    border: 1px solid var(--border); margin-bottom: 0.6rem;
}

/* ── Availability rows ── */
.avail-row {
    display: flex; align-items: center; gap: 0.45rem;
    font-size: 0.74rem; font-weight: 600; margin-bottom: 0.28rem;
}
.avail-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.avail-yes .avail-dot { background: var(--success); }
.avail-no  .avail-dot { background: var(--danger); }
.avail-yes { color: var(--success); }
.avail-no  { color: var(--danger); }

/* ── 3-col action row: rent | buy | view ── */
.book-actions-3 {
    display: grid; grid-template-columns: 1fr 1fr auto;
    gap: 0.5rem; margin-top: auto;
}
.btn-view {
    padding: 0.65rem 0.75rem; border-radius: var(--radius-sm);
    font-family: 'Outfit', sans-serif; font-size: 0.8rem; font-weight: 700;
    cursor: pointer; display: flex; align-items: center; justify-content: center;
    gap: 0.35rem; transition: all var(--t-fast); text-decoration: none;
    background: var(--accent-soft); color: var(--accent);
    border: 1.5px solid rgba(245,176,66,0.22);
}
.btn-view:hover { background: var(--accent); color: #fff; border-color: var(--accent); }

/* ── Card stagger animation ── */
.book-card { animation: cardIn .38s ease both; }
.book-card:nth-child(1){animation-delay:.04s}
.book-card:nth-child(2){animation-delay:.08s}
.book-card:nth-child(3){animation-delay:.12s}
.book-card:nth-child(4){animation-delay:.16s}
.book-card:nth-child(5){animation-delay:.20s}
.book-card:nth-child(6){animation-delay:.24s}
.book-card:nth-child(7){animation-delay:.28s}
.book-card:nth-child(8){animation-delay:.32s}
@keyframes cardIn {
    from { opacity:0; transform:translateY(18px); }
    to   { opacity:1; transform:none; }
}
</style>
{% endblock %}


{% block content %}

<!-- ══════════════════════════════════════
     FILTER BAR
     ══════════════════════════════════════ -->
<div class="filter-bar" style="flex-direction:column;align-items:flex-start;gap:0.75rem;">

    <!-- Row 1 — label + genre/availability pills -->
    <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;width:100%;">
        <span class="filter-label">Browse by</span>
        <div class="filter-tags">

            <a href="?{% if search_query %}search={{ search_query }}&{% endif %}"
               class="filter-tag {% if not selected_genre and not selected_store and not selected_availability %}active{% endif %}">
                <i class="bi bi-grid-3x3-gap"></i> All Books
            </a>

            <a href="?{% if search_query %}search={{ search_query }}&{% endif %}availability=rent"
               class="filter-tag {% if selected_availability == 'rent' %}active{% endif %}">
                <i class="bi bi-arrow-repeat"></i> For Rent
            </a>

            <a href="?{% if search_query %}search={{ search_query }}&{% endif %}availability=buy"
               class="filter-tag {% if selected_availability == 'buy' %}active{% endif %}">
                <i class="bi bi-bag-check"></i> For Sale
            </a>

            {% for genre in genres %}
            <a href="?{% if search_query %}search={{ search_query }}&{% endif %}genre={{ genre }}"
               class="filter-tag {% if selected_genre == genre %}active{% endif %}">
                {{ genre }}
            </a>
            {% endfor %}

        </div>
    </div>

    <!-- Row 2 — store dropdown + clear all -->
    <div class="filter-row2">
        <label for="store-filter">
            <i class="bi bi-shop-window"></i> Filter by store
        </label>
        <select id="store-filter" class="bh-select"
                onchange="(function(v){const u=new URL(window.location.href);v?u.searchParams.set('store',v):u.searchParams.delete('store');window.location.href=u.toString()})(this.value)">
            <option value="">All Stores</option>
            {% for store in stores %}
            <option value="{{ store.id }}"
                    {% if selected_store == store.id|stringformat:'s' %}selected{% endif %}>
                {{ store.store_name }}
            </option>
            {% endfor %}
        </select>

        {% if search_query or selected_genre or selected_store or selected_availability %}
        <a href="{% url 'customer_dashboard' %}"
           class="nav-btn" style="margin-left:auto;color:var(--danger);background:var(--danger-soft);border-color:rgba(255,77,109,0.22);">
            <i class="bi bi-x-circle-fill"></i> Clear All
        </a>
        {% endif %}
    </div>

</div>


<!-- ══════════════════════════════════════
     RESULTS BAR
     ══════════════════════════════════════ -->
<div class="results-bar">
    <div style="flex:1;">
        <div class="results-text">
            Found <strong>{{ total_books }}</strong> book{{ total_books|pluralize }}
            {% if search_query %}matching <span class="hl">"{{ search_query }}"</span>{% endif %}
        </div>

        <!-- Active pills -->
        {% if selected_genre or selected_store or selected_availability %}
        <div class="active-pills">
            {% if selected_genre %}
            <span class="active-pill pill-blue">
                <i class="bi bi-tag-fill"></i> {{ selected_genre }}
                <a href="?{% if search_query %}search={{ search_query }}&{% endif %}" class="pill-close">×</a>
            </span>
            {% endif %}
            {% if selected_availability %}
            <span class="active-pill pill-green">
                <i class="bi bi-check-circle-fill"></i>
                {% if selected_availability == 'rent' %}For Rent{% else %}For Sale{% endif %}
                <a href="?{% if search_query %}search={{ search_query }}&{% endif %}" class="pill-close">×</a>
            </span>
            {% endif %}
            {% if selected_store %}
            <span class="active-pill pill-purple">
                <i class="bi bi-shop"></i>
                {% for store in stores %}{% if store.id|stringformat:'s' == selected_store %}{{ store.store_name }}{% endif %}{% endfor %}
                <a href="?{% if search_query %}search={{ search_query }}&{% endif %}" class="pill-close">×</a>
            </span>
            {% endif %}
        </div>
        {% endif %}

        {% if search_query and total_books == 0 %}
        <div style="margin-top:.6rem;font-size:.82rem;color:var(--danger);display:flex;align-items:center;gap:.4rem;">
            <i class="bi bi-exclamation-circle-fill"></i>
            No results found. Try different keywords or remove filters.
        </div>
        {% endif %}
    </div>

    {% if search_query %}
    <a href="{% url 'customer_dashboard' %}" class="nav-btn" style="flex-shrink:0;">
        <i class="bi bi-x"></i> Clear Search
    </a>
    {% endif %}
</div>


<!-- ══════════════════════════════════════
     SECTION HEADING
     ══════════════════════════════════════ -->
<div class="section-hd">
    <div class="section-hd-left">
        <div class="section-icon">
            {% if search_query %}<i class="bi bi-search"></i>
            {% elif selected_genre %}<i class="bi bi-tag-fill"></i>
            {% else %}<i class="bi bi-collection-fill"></i>{% endif %}
        </div>
        <div>
            <div class="section-title">
                {% if search_query %}Search Results
                {% elif selected_genre %}{{ selected_genre }}
                {% elif selected_availability == 'rent' %}Books for Rent
                {% elif selected_availability == 'buy' %}Books for Sale
                {% else %}All Books{% endif %}
            </div>
            <div class="section-sub">{{ total_books }} book{{ total_books|pluralize }} available</div>
        </div>
    </div>
</div>


<!-- ══════════════════════════════════════
     BOOKS GRID
     ══════════════════════════════════════ -->
<div class="book-grid">

{% for book in books %}
<div class="book-card">

    <!-- Cover image -->
    <div class="book-img">
        {% if book.store %}
        <span class="store-badge">{{ book.store.store_name|default:"BookHub" }}</span>
        {% endif %}

        <button class="book-wish" aria-label="Save to wishlist">
            <i class="bi bi-heart"></i>
        </button>

        <a href="{% url 'book_detail' book.id %}" class="quick-view">
            <i class="bi bi-eye"></i> Quick View
        </a>

        {% if book.cover_image %}
        <img src="{{ book.cover_image.url }}"
             alt="{{ book.title }}"
             loading="lazy"
             onerror="this.onerror=null;this.src='{% static 'assets/img/portfolio/books-1.jpg' %}';">
        {% else %}
        <img src="{% static 'assets/img/portfolio/books-1.jpg' %}"
             alt="{{ book.title }}"
             loading="lazy">
        {% endif %}
    </div>

    <!-- Card body -->
    <div class="book-body">

        {% if book.genre %}
        <span class="book-genre-tag">{{ book.genre }}</span>
        {% endif %}

        <div class="book-title">{{ book.title }}</div>
        <div class="book-author">{{ book.author }}</div>

        <!-- Pricing -->
        <div class="pricing-row">
            <div class="price-pill price-rent">
                <span class="price-tag">Rent</span>
                <span class="price-amount">${{ book.rental_price }}</span>
                <span class="price-period">/month</span>
            </div>
            <div class="price-pill price-buy">
                <span class="price-tag">Buy</span>
                <span class="price-amount">${{ book.sale_price }}</span>
                <span class="price-period">one-time</span>
            </div>
        </div>

        <!-- Availability -->
        <div style="margin-bottom:1rem;">
            <div class="avail-row {% if book.available_copies > 0 %}avail-yes{% else %}avail-no{% endif %}">
                <span class="avail-dot"></span>
                {% if book.available_copies > 0 %}
                    {{ book.available_copies }} available for rent
                {% else %}
                    Not available for rent
                {% endif %}
            </div>
            <div class="avail-row {% if book.available_sales > 0 %}avail-yes{% else %}avail-no{% endif %}">
                <span class="avail-dot"></span>
                {% if book.available_sales > 0 %}
                    {{ book.available_sales }} available to buy
                {% else %}
                    Not available to buy
                {% endif %}
            </div>
        </div>

        <!-- Action buttons -->
        <div class="book-actions-3">

            {% if book.available_copies > 0 %}
            <a href="{% url 'add_to_cart_rent' book.id %}" class="btn btn-rent">
                <i class="bi bi-arrow-repeat"></i> Rent
            </a>
            {% else %}
            <button class="btn btn-disabled" disabled>
                <i class="bi bi-arrow-repeat"></i> Rent
            </button>
            {% endif %}

            {% if book.available_sales > 0 %}
            <a href="{% url 'add_to_cart_buy' book.id %}" class="btn btn-buy">
                <i class="bi bi-bag-check"></i> Buy
            </a>
            {% else %}
            <button class="btn btn-disabled" disabled>
                <i class="bi bi-bag-check"></i> Buy
            </button>
            {% endif %}

            <a href="{% url 'book_detail' book.id %}" class="btn-view">
                <i class="bi bi-eye-fill"></i>
            </a>

        </div>

    </div><!-- /book-body -->
</div><!-- /book-card -->

{% empty %}
<div class="empty-state">
    <div class="empty-icon"><i class="bi bi-search"></i></div>
    <h3>No books found</h3>
    <p>Try different keywords or clear the active filters to see all books.</p>
    <a href="{% url 'customer_dashboard' %}" class="nav-pill" style="display:inline-flex;">
        <i class="bi bi-x-circle"></i> Clear All Filters
    </a>
</div>
{% endfor %}

</div><!-- /book-grid -->


<!-- ══════════════════════════════════════
     PAGINATION
     ══════════════════════════════════════ -->
{% if books.has_other_pages %}
<div class="bh-pagination">
    {% if books.has_previous %}
    <a class="page-btn"
       href="?page={{ books.previous_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if selected_genre %}&genre={{ selected_genre }}{% endif %}{% if selected_store %}&store={{ selected_store }}{% endif %}{% if selected_availability %}&availability={{ selected_availability }}{% endif %}">
        <i class="bi bi-chevron-left"></i> Previous
    </a>
    {% endif %}

    <span class="page-btn current">
        Page {{ books.number }} of {{ books.paginator.num_pages }}
    </span>

    {% if books.has_next %}
    <a class="page-btn"
       href="?page={{ books.next_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if selected_genre %}&genre={{ selected_genre }}{% endif %}{% if selected_store %}&store={{ selected_store }}{% endif %}{% if selected_availability %}&availability={{ selected_availability }}{% endif %}">
        Next <i class="bi bi-chevron-right"></i>
    </a>
    {% endif %}
</div>
{% endif %}

{% endblock %}


{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function () {

    // ── Wishlist heart toggle (visual; wire to your API endpoint as needed) ──
    document.querySelectorAll('.book-wish').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault(); e.stopPropagation();
            const icon = this.querySelector('i');
            const on = icon.classList.contains('bi-heart-fill');
            icon.className = on ? 'bi bi-heart' : 'bi bi-heart-fill';
            this.style.background  = on ? '' : 'var(--danger)';
            this.style.color       = on ? '' : '#fff';
            this.style.borderColor = on ? '' : 'var(--danger)';
            this.style.opacity     = '1';
        });
    });

    // ── Cart count refresh ──
    fetch('/get-cart-count/')
        .then(r => r.json())
        .then(d => {
            const el = document.getElementById('cart-count');
            if (el) el.textContent = d.count || 0;
        })
        .catch(() => {});

});
</script>
{% endblock %}
