from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Features, Store, Book
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book, Store, add_book_registration

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from datetime import datetime, timedelta



class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


def index(request):
    feature = Features.objects.all()
    return render(request, 'index.html', {'features': feature})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Registration successful! Please log in.")
                return redirect('login')
        else:
            messages.info(request, "Password not matching")
            return redirect('register')

    return render(request, "register.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store_dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, "login.html")


def logout(request):
    auth_logout(request)
    return redirect('index')


def post(request, pk):
    return render(request, "post.html", {"pk": pk})


@csrf_exempt
def store(request):
    if request.method == 'POST':
        messages.success(request, 'Store registration received (stub).')
        return redirect('index')

    return render(request, 'store/registration.html')


@csrf_exempt
def store_registration(request):
    if request.method == "POST":
        store_name = request.POST.get("store_name")
        owner_full_name = request.POST.get("owner_full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        store_type = request.POST.get("store_type")
        city = request.POST.get("city")
        address = request.POST.get("address")
        store_description = request.POST.get("store_description")
        offers_rental = request.POST.get("offers_rental")
        offers_sale = request.POST.get("offers_sale")
        offers_delivery = request.POST.get("offers_delivery")
        delivery_radius = request.POST.get("delivery_radius")
        delivery_fee = request.POST.get("delivery_fee")
        delivery_bike = request.POST.get("delivery_bike")
        delivery_car = request.POST.get("delivery_car")
        delivery_pickup = request.POST.get("delivery_pickup")

        open_monday = request.POST.get("open_monday")
        open_time_monday = request.POST.get("open_time_monday")
        close_time_monday = request.POST.get("close_time_monday")

        open_tuesday = request.POST.get("open_tuesday")
        open_time_tuesday = request.POST.get("open_time_tuesday")
        close_time_tuesday = request.POST.get("close_time_tuesday")

        open_wednesday = request.POST.get("open_wednesday")
        open_time_wednesday = request.POST.get("open_time_wednesday")
        close_time_wednesday = request.POST.get("close_time_wednesday")

        open_thursday = request.POST.get("open_thursday")
        open_time_thursday = request.POST.get("open_time_thursday")
        close_time_thursday = request.POST.get("close_time_thursday")

        open_friday = request.POST.get("open_friday")
        open_time_friday = request.POST.get("open_time_friday")
        close_time_friday = request.POST.get("close_time_friday")

        open_saturday = request.POST.get("open_saturday")
        open_time_saturday = request.POST.get("open_time_saturday")
        close_time_saturday = request.POST.get("close_time_saturday")

        open_sunday = request.POST.get("open_sunday")
        open_time_sunday = request.POST.get("open_time_sunday")
        close_time_sunday = request.POST.get("close_time_sunday")

        def to_bool(v):
            return True if v in ("on", "true", "True", "1", True) else False

        def none_if_empty(v):
            return None if v in (None, "") else v

        offers_rental = to_bool(offers_rental)
        offers_sale = to_bool(offers_sale)
        offers_delivery = to_bool(offers_delivery)
        delivery_bike = to_bool(delivery_bike)
        delivery_car = to_bool(delivery_car)
        delivery_pickup = to_bool(delivery_pickup)
        open_monday = to_bool(open_monday)
        open_tuesday = to_bool(open_tuesday)
        open_wednesday = to_bool(open_wednesday)
        open_thursday = to_bool(open_thursday)
        open_friday = to_bool(open_friday)
        open_saturday = to_bool(open_saturday)
        open_sunday = to_bool(open_sunday)

        rental_period = none_if_empty(request.POST.get("rental_period"))
        rental_price = none_if_empty(request.POST.get("rental_price"))
        late_fee = none_if_empty(request.POST.get("late_fee"))
        security_deposit = none_if_empty(request.POST.get("security_deposit"))
        max_books_raw = none_if_empty(request.POST.get("max_books"))
        max_books = int(max_books_raw) if max_books_raw is not None else None
        discount_percent = none_if_empty(request.POST.get("discount_percent"))
        payment_methods = none_if_empty(request.POST.get("payment_methods"))
        agree_terms = to_bool(request.POST.get("agree_terms"))

        if store_name and owner_full_name:
            if Store.objects.filter(store_name=store_name).exists():
                messages.info(request, "store name already exists")
                return redirect('register')
            elif Store.objects.filter(owner_full_name=owner_full_name).exists():
                messages.info(request, "Owner full name already exists")
                return redirect('register')
            else:
                store = Store.objects.create(
                    store_name=store_name,
                    owner_full_name=owner_full_name,
                    email=email,
                    phone=phone,
                    store_type=store_type,
                    city=city,
                    address=address,
                    store_description=store_description,
                    offers_rental=offers_rental,
                    offers_sale=offers_sale,
                    offers_delivery=offers_delivery,
                    delivery_radius=delivery_radius,
                    delivery_fee=delivery_fee,
                    delivery_bike=delivery_bike,
                    delivery_car=delivery_car,
                    delivery_pickup=delivery_pickup,
                    open_monday=open_monday,
                    open_time_monday=open_time_monday,
                    close_time_monday=close_time_monday,
                    open_tuesday=open_tuesday,
                    open_time_tuesday=open_time_tuesday,
                    close_time_tuesday=close_time_tuesday,
                    open_wednesday=open_wednesday,
                    open_time_wednesday=open_time_wednesday,
                    close_time_wednesday=close_time_wednesday,
                    open_thursday=open_thursday,
                    open_time_thursday=open_time_thursday,
                    close_time_thursday=close_time_thursday,
                    open_friday=open_friday,
                    open_time_friday=open_time_friday,
                    close_time_friday=close_time_friday,
                    open_saturday=open_saturday,
                    open_time_saturday=open_time_saturday,
                    close_time_saturday=close_time_saturday,
                    open_sunday=open_sunday,
                    open_time_sunday=open_time_sunday,
                    close_time_sunday=close_time_sunday,
                    rental_period=rental_period,
                    rental_price=rental_price,
                    late_fee=late_fee,
                    security_deposit=security_deposit,
                    max_books=max_books,
                    discount_percent=discount_percent,
                    payment_methods=payment_methods,
                    agree_terms=agree_terms,
                )
                store.save()
                messages.success(request, "Registration successful! Please log in.")
                return redirect('store_registration_view')
        else:
            messages.info(request, "Store name and owner full name are required")
            return redirect('store')

    return render(request, "store/registration.html")


def counter(request):
    posts = [1, 2, 3, 4, 5, 6]
    return render(request, "counter.html", {"posts": posts})


# Customer: Store list view
def store_list(request):
    stores = Store.objects.all()

    # Filter by city
    city_filter = request.GET.get('city', '')
    if city_filter:
        stores = stores.filter(city__icontains=city_filter)

    # Filter by service type
    service_filter = request.GET.get('service', '')
    if service_filter == 'rent':
        stores = stores.filter(offers_rental=True)
    elif service_filter == 'buy':
        stores = stores.filter(offers_sale=True)
    elif service_filter == 'delivery':
        stores = stores.filter(offers_delivery=True)

    context = {
        'stores': stores,
        'cities': Store.objects.values_list('city', flat=True).distinct(),
        'selected_city': city_filter,
        'selected_service': service_filter,
    }

    return render(request, 'customer/store_list.html', context)


# Customer: Store detail view
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    # Get books available in this store
    books = Book.objects.filter(store=store)

    # Separate rental and sale books
    rental_books = books.filter(available_copies__gt=0)
    sale_books = books.filter(available_sales__gt=0)

    # Get store opening hours
    opening_hours = []
    days = [
        ('monday', 'Monday', store.open_monday, store.open_time_monday, store.close_time_monday),
        ('tuesday', 'Tuesday', store.open_tuesday, store.open_time_tuesday, store.close_time_tuesday),
        ('wednesday', 'Wednesday', store.open_wednesday, store.open_time_wednesday, store.close_time_wednesday),
        ('thursday', 'Thursday', store.open_thursday, store.open_time_thursday, store.close_time_thursday),
        ('friday', 'Friday', store.open_friday, store.open_time_friday, store.close_time_friday),
        ('saturday', 'Saturday', store.open_saturday, store.open_time_saturday, store.close_time_saturday),
        ('sunday', 'Sunday', store.open_sunday, store.open_time_sunday, store.close_time_sunday),
    ]

    for day_name, day_display, is_open, open_time, close_time in days:
        if is_open and open_time and close_time:
            try:
                hours = f"{open_time.strftime('%I:%M %p')} - {close_time.strftime('%I:%M %p')}"
            except Exception:
                hours = f"{open_time} - {close_time}"
            opening_hours.append({'day': day_display, 'hours': hours})
        elif is_open:
            opening_hours.append({'day': day_display, 'hours': "Open (Hours not specified)"})
        else:
            opening_hours.append({'day': day_display, 'hours': "Closed"})

    context = {
        'store': store,
        'books': books,
        'rental_books': rental_books,
        'sale_books': sale_books,
        'opening_hours': opening_hours,
    }

    return render(request, 'customer/store_detail.html', context)



def dashboard(request):
    context = {
        'page_title': 'Dashboard',
        'store_name': 'My Book Store',
        'user_name': 'Admin',
        'revenue_today': 250,
        'total_books': 500,
        'active_rentals': 23,
        'pending_deliveries': 8,
        'new_customers': 3,
        'recent_orders': [
            {'id': 'ORD-1001', 'customer': 'John Doe', 'items': '2 books', 'status': 'Processing', 'delivery': 'Tomorrow 10 AM'},
            {'id': 'ORD-1002', 'customer': 'Jane Smith', 'items': '1 book rental', 'status': 'Ready for Pickup', 'delivery': 'Store Pickup'},
        ],
        'alerts': [
            {'type': 'danger', 'title': 'Low Stock Alert', 'message': '"1984" by George Orwell - Only 2 copies left', 'action': 'Reorder Now'},
            {'type': 'warning', 'title': 'Rentals Expiring Soon', 'message': '5 rentals due tomorrow', 'action': 'Send Reminders'},
        ],
    }
    return render(request, 'dashboard.html', context)


def store_dashboard(request):
    context = {'page_title': 'Store Dashboard', 'store_metrics': {'revenue_today': 120, 'active_rentals': 12, 'pending_deliveries': 4}}
    return render(request, 'store/dashboard.html', context)


def add_book(request):
    if request.method == 'POST':
        messages.success(request, 'Book added (stub).')
        return redirect('store_dashboard')
    return render(request, "store/add_book.html")


def view_inventory(request):
    books = Book.objects.all()
    return render(request, 'store/view_inventory.html', {'books': books})


def add_book_registration(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        genre = request.POST.get("genre")
        publication_year = request.POST.get("publication_year")
        total_copies = request.POST.get("total_copies") or 0
        available_copies = request.POST.get("availble_rent") or 0
        available_sales = request.POST.get("availble_sale") or 0
        rental_price = request.POST.get("rental_price") or 0
        sale_price = request.POST.get("sale_price") or 0

        if title and author:
            if Book.objects.filter(title=title, author=author).exists():
                messages.info(request, "Book already exists")
                return redirect('add_book')
            else:
                book = Book.objects.create(
                    title=title,
                    author=author,
                    genre=genre,
                    publication_year=publication_year or None,
                    total_copies=total_copies,
                    available_copies=available_copies,
                    available_sales=available_sales,
                    rental_price=rental_price,
                    sale_price=sale_price,
                )
                book.save()
                messages.success(request, "Book added successfully.")
                return redirect('add_book_registration')

        messages.info(request, "Title and Author are required")
        return redirect('add_book')

    return render(request, "store/add_book.html")
        




































        
# views.py - Update the edit_book function
def edit_book(request, id):
    book = Book.objects.get(pk=id)
    
    if request.method == 'POST':
        # Handle the form submission
        title = request.POST.get("title")
        author = request.POST.get("author")
        genre = request.POST.get("genre")
        publication_year = request.POST.get("publication_year")
        total_copies = request.POST.get("total_copies") or 0
        available_copies = request.POST.get("available_rent") or 0  # Fixed: changed from "availble_rent"
        available_sales = request.POST.get("available_sale") or 0   # Fixed: changed from "availble_sale"
        rental_price = request.POST.get("rental_price") or 0
        sale_price = request.POST.get("sale_price") or 0
        
        # Update the book object
        book.title = title
        book.author = author
        book.genre = genre
        book.publication_year = publication_year or None
        book.total_copies = total_copies
        book.available_copies = available_copies
        book.available_sales = available_sales
        book.rental_price = rental_price
        book.sale_price = sale_price
        
        book.save()
        messages.success(request, "Book updated successfully.")
        return redirect('view_inventory')
    
    # GET request - show form with existing data
    return render(request, 'store/edit_book.html', {'book': book})
















#store registration view and edit   and  delete


def store_registration_view(request):
    stores = Store.objects.all()
    return render(request, 'store/registration/registration_view.html', {'stores': stores})


def edit_store(request, id):
    try:
        store = Store.objects.get(pk=id)
    except Store.DoesNotExist:
        messages.error(request, "Store not found.")
        return redirect('store_registration_view')

    if request.method == 'POST':
        def to_bool(v):
            return True if v in ("on", "true", "True", "1", True) else False

        def none_if_empty(v):
            return None if v in (None, "") else v

        store.store_name = request.POST.get('store_name') or store.store_name
        store.owner_full_name = request.POST.get('owner_full_name') or store.owner_full_name
        store.email = request.POST.get('email') or store.email
        store.phone = request.POST.get('phone') or store.phone
        store.store_type = request.POST.get('store_type') or store.store_type
        store.city = request.POST.get('city') or store.city
        store.address = request.POST.get('address') or store.address
        store.store_description = request.POST.get('store_description') or store.store_description

        store.offers_rental = to_bool(request.POST.get('offers_rental'))
        store.offers_sale = to_bool(request.POST.get('offers_sale'))
        store.offers_delivery = to_bool(request.POST.get('offers_delivery'))
        store.delivery_radius = none_if_empty(request.POST.get('delivery_radius')) or store.delivery_radius
        store.delivery_fee = none_if_empty(request.POST.get('delivery_fee')) or store.delivery_fee
        store.delivery_bike = to_bool(request.POST.get('delivery_bike'))
        store.delivery_car = to_bool(request.POST.get('delivery_car'))
        store.delivery_pickup = to_bool(request.POST.get('delivery_pickup'))

        # opening days
        store.open_monday = to_bool(request.POST.get('open_monday'))
        store.open_time_monday = none_if_empty(request.POST.get('open_time_monday')) or store.open_time_monday
        store.close_time_monday = none_if_empty(request.POST.get('close_time_monday')) or store.close_time_monday

        store.open_tuesday = to_bool(request.POST.get('open_tuesday'))
        store.open_time_tuesday = none_if_empty(request.POST.get('open_time_tuesday')) or store.open_time_tuesday
        store.close_time_tuesday = none_if_empty(request.POST.get('close_time_tuesday')) or store.close_time_tuesday

        store.open_wednesday = to_bool(request.POST.get('open_wednesday'))
        store.open_time_wednesday = none_if_empty(request.POST.get('open_time_wednesday')) or store.open_time_wednesday
        store.close_time_wednesday = none_if_empty(request.POST.get('close_time_wednesday')) or store.close_time_wednesday

        store.open_thursday = to_bool(request.POST.get('open_thursday'))
        store.open_time_thursday = none_if_empty(request.POST.get('open_time_thursday')) or store.open_time_thursday
        store.close_time_thursday = none_if_empty(request.POST.get('close_time_thursday')) or store.close_time_thursday

        store.open_friday = to_bool(request.POST.get('open_friday'))
        store.open_time_friday = none_if_empty(request.POST.get('open_time_friday')) or store.open_time_friday
        store.close_time_friday = none_if_empty(request.POST.get('close_time_friday')) or store.close_time_friday

        store.open_saturday = to_bool(request.POST.get('open_saturday'))
        store.open_time_saturday = none_if_empty(request.POST.get('open_time_saturday')) or store.open_time_saturday
        store.close_time_saturday = none_if_empty(request.POST.get('close_time_saturday')) or store.close_time_saturday

        store.open_sunday = to_bool(request.POST.get('open_sunday'))
        store.open_time_sunday = none_if_empty(request.POST.get('open_time_sunday')) or store.open_time_sunday
        store.close_time_sunday = none_if_empty(request.POST.get('close_time_sunday')) or store.close_time_sunday

        # additional numeric/optional fields
        rental_period = none_if_empty(request.POST.get('rental_period'))
        store.rental_period = rental_period or store.rental_period
        rental_price = none_if_empty(request.POST.get('rental_price'))
        store.rental_price = rental_price or store.rental_price
        store.late_fee = none_if_empty(request.POST.get('late_fee')) or store.late_fee
        store.security_deposit = none_if_empty(request.POST.get('security_deposit')) or store.security_deposit
        max_books_raw = none_if_empty(request.POST.get('max_books'))
        store.max_books = int(max_books_raw) if max_books_raw is not None else store.max_books
        store.discount_percent = none_if_empty(request.POST.get('discount_percent')) or store.discount_percent
        store.payment_methods = none_if_empty(request.POST.get('payment_methods')) or store.payment_methods
        store.agree_terms = to_bool(request.POST.get('agree_terms'))

        store.save()
        messages.success(request, "Store updated successfully.")
        return redirect('store_registration_view')

    return render(request, 'store/registration/registration_update.html', {'store': store})










































def delete_store(request, id):
    try:
        store = Store.objects.get(pk=id)
    except Store.DoesNotExist:
        messages.error(request, "Store not found.")
        return redirect('store_registration_view')

    store.delete()
    messages.success(request, "Store deleted.")
    return redirect('store_registration_view')






























def book_delete(request, id):
    book = Book.objects.get(pk=id)
    book.delete()
    return redirect('view_inventory')





  








































































  # Update the customer_dashboard view with pagination
def customer_dashboard(request):
    # Ensure any store-added `add_book_registration` rows are present in `Book` model.
    try:
        existing = Book.objects.values_list('title', 'author')
        existing_set = set(existing)
        for ab in add_book_registration.objects.select_related('store').all():
            key = (ab.title, ab.author)
            if key not in existing_set:
                Book.objects.create(
                    title=ab.title,
                    author=ab.author,
                    genre=getattr(ab, 'genre', 'fiction') or 'fiction',
                    publication_year=ab.publication_year,
                    total_copies=ab.total_copies or 0,
                    available_copies=ab.available_copies or 0,
                    available_sales=ab.available_sales or 0,
                    rental_price=ab.rental_price or 0,
                    sale_price=ab.sale_price or 0,
                    store=ab.store if hasattr(ab, 'store') else None,
                )
        
    except Exception:
        # Fall back silently if migration step fails for any reason
        pass

    # Get all books
    books = Book.objects.select_related('store').all()
    
    # Get distinct genres for filtering
    genres = Book.objects.values_list('genre', flat=True).distinct()
    
    # Get all stores for filtering
    stores = Store.objects.all()
    
    # Search functionality (title only)
    search_query = request.GET.get('search', '')
    # Trim whitespace to avoid empty/no-match queries from accidental spaces
    search_query = search_query.strip()
    if search_query:
        books = books.filter(title__icontains=search_query)
    
    # Filter by genre
    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        books = books.filter(genre=genre_filter)
    
    # Filter by store
    store_filter = request.GET.get('store', '')
    if store_filter:
        books = books.filter(store_id=store_filter)
    
    # Filter by availability (rental or sale)
    availability_filter = request.GET.get('availability', '')
    if availability_filter == 'rent':
        books = books.filter(available_copies__gt=0)
    elif availability_filter == 'buy':
        books = books.filter(available_sales__gt=0)
    
    # Sort functionality
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        books = books.order_by('sale_price')
    elif sort_by == 'price_high':
        books = books.order_by('-sale_price')
    elif sort_by == 'title':
        books = books.order_by('title')
    elif sort_by == 'author':
        books = books.order_by('author')
    else:  # newest
        books = books.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(books, 12)  # Show 12 books per page
    page_number = request.GET.get('page', 1)
    
    try:
        books_page = paginator.page(page_number)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)
    
    # Get featured books (most recent 4)
    featured_books = Book.objects.select_related('store').order_by('-created_at')[:4]
    # Debug info to help verify search behavior in template
    debug_count = books.count()
    try:
        debug_titles = list(books.values_list('title', flat=True)[:50])
    except Exception:
        debug_titles = []
    
    context = {
        'books': books_page,
        'featured_books': featured_books,
        'genres': genres,
        'stores': stores,
        'search_query': search_query,
        'selected_genre': genre_filter,
        'selected_store': store_filter,
        'selected_availability': availability_filter,
        'sort_by': sort_by,
        'total_books': books.count(),
        'debug_count': debug_count,
        'debug_titles': debug_titles,
        'paginator': paginator,
    }
    
    return render(request, 'customer/dashboard.html', context)

# Enhanced book detail view with cart functionality
def book_detail(request, book_id):
    book = get_object_or_404(Book.objects.select_related('store'), id=book_id)
    
    # Get similar books (same genre)
    similar_books = Book.objects.filter(
        genre=book.genre
    ).exclude(id=book_id).select_related('store')[:4]
    
    # Check if user can rent or buy
    can_rent = book.available_copies > 0
    can_buy = book.available_sales > 0
    
    # Get store details
    store = book.store
    opening_hours = []
    if store:
        days = [
            ('monday', 'Monday', store.open_monday, store.open_time_monday, store.close_time_monday),
            ('tuesday', 'Tuesday', store.open_tuesday, store.open_time_tuesday, store.close_time_tuesday),
            ('wednesday', 'Wednesday', store.open_wednesday, store.open_time_wednesday, store.close_time_wednesday),
            ('thursday', 'Thursday', store.open_thursday, store.open_time_thursday, store.close_time_thursday),
            ('friday', 'Friday', store.open_friday, store.open_time_friday, store.close_time_friday),
            ('saturday', 'Saturday', store.open_saturday, store.open_time_saturday, store.close_time_saturday),
            ('sunday', 'Sunday', store.open_sunday, store.open_time_sunday, store.close_time_sunday),
        ]
        
        for day_name, day_display, is_open, open_time, close_time in days:
            if is_open and open_time and close_time:
                opening_hours.append({
                    'day': day_display,
                    'hours': f"{open_time.strftime('%I:%M %p')} - {close_time.strftime('%I:%M %p')}"
                })
            elif is_open:
                opening_hours.append({
                    'day': day_display,
                    'hours': "Open"
                })
    
    # Check if book is in user's wishlist (placeholder)
    in_wishlist = False
    
    context = {
        'book': book,
        'similar_books': similar_books,
        'can_rent': can_rent,
        'can_buy': can_buy,
        'store': store,
        'opening_hours': opening_hours,
        'in_wishlist': in_wishlist,
    }
    
    return render(request, 'customer/book_detail.html', context)

# Shopping Cart with session management
def shopping_cart(request):
    # Get cart from session
    cart = request.session.get('cart', {'rental': [], 'purchase': []})
    
    cart_items = []
    total_price = 0
    
    # Process rental items
    for item_id in cart['rental']:
        try:
            book = Book.objects.get(id=item_id)
            cart_items.append({
                'book': book,
                'type': 'rental',
                'price': book.rental_price,
                'period': '1 month',  # Default period
            })
            total_price += float(book.rental_price)
        except Book.DoesNotExist:
            pass
    
    # Process purchase items
    for item_id in cart['purchase']:
        try:
            book = Book.objects.get(id=item_id)
            cart_items.append({
                'book': book,
                'type': 'purchase',
                'price': book.sale_price,
            })
            total_price += float(book.sale_price)
        except Book.DoesNotExist:
            pass
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': len(cart_items),
    }
    
    return render(request, 'customer/cart.html', context)

# Update add_to_cart functions with session management
def add_to_cart_rent(request, book_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to add items to cart.")
        return redirect('login')
    
    book = get_object_or_404(Book, id=book_id)
    
    if book.available_copies <= 0:
        messages.error(request, "This book is not available for rent at the moment.")
        return redirect('book_detail', book_id=book_id)
    
    # Initialize cart in session if not exists
    if 'cart' not in request.session:
        request.session['cart'] = {'rental': [], 'purchase': []}
    
    cart = request.session['cart']
    
    # Check if already in cart
    if book_id not in cart['rental']:
        cart['rental'].append(book_id)
        request.session.modified = True
        messages.success(request, f"Added '{book.title}' to your rental cart!")
    else:
        messages.info(request, f"'{book.title}' is already in your cart.")
    
    return redirect('book_detail', book_id=book_id)

def add_to_cart_buy(request, book_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to add items to cart.")
        return redirect('login')
    
    book = get_object_or_404(Book, id=book_id)
    
    if book.available_sales <= 0:
        messages.error(request, "This book is not available for purchase at the moment.")
        return redirect('book_detail', book_id=book_id)
    
    # Initialize cart in session if not exists
    if 'cart' not in request.session:
        request.session['cart'] = {'rental': [], 'purchase': []}
    
    cart = request.session['cart']
    
    # Check if already in cart
    if book_id not in cart['purchase']:
        cart['purchase'].append(book_id)
        request.session.modified = True
        messages.success(request, f"Added '{book.title}' to your purchase cart!")
    else:
        messages.info(request, f"'{book.title}' is already in your cart.")
    
    return redirect('book_detail', book_id=book_id)

def remove_from_cart(request, book_id, item_type):
    if 'cart' in request.session:
        cart = request.session['cart']
        
        if item_type == 'rental' and book_id in cart['rental']:
            cart['rental'].remove(book_id)
        elif item_type == 'purchase' and book_id in cart['purchase']:
            cart['purchase'].remove(book_id)
        
        request.session.modified = True
        messages.success(request, "Item removed from cart.")
    
    return redirect('shopping_cart')

# Checkout process
def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to checkout.")
        return redirect('login')
    
    cart = request.session.get('cart', {'rental': [], 'purchase': []})
    
    if not cart['rental'] and not cart['purchase']:
        messages.warning(request, "Your cart is empty.")
        return redirect('customer_dashboard')
    
    # Get cart items
    rental_items = Book.objects.filter(id__in=cart['rental'])
    purchase_items = Book.objects.filter(id__in=cart['purchase'])
    
    # Calculate totals
    rental_total = sum(float(item.rental_price) for item in rental_items)
    purchase_total = sum(float(item.sale_price) for item in purchase_items)
    total = rental_total + purchase_total
    
    # Get user's saved addresses (placeholder)
    addresses = []
    
    context = {
        'rental_items': rental_items,
        'purchase_items': purchase_items,
        'rental_total': rental_total,
        'purchase_total': purchase_total,
        'total': total,
        'addresses': addresses,
    }
    
    return render(request, 'customer/checkout.html', context)

def process_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please login to place order'})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Here you would create an Order model instance
            # For now, just clear the cart
            if 'cart' in request.session:
                del request.session['cart']
            
            return JsonResponse({
                'success': True,
                'message': 'Order placed successfully!',
                'order_id': 'ORD-' + str(datetime.now().timestamp()).replace('.', '')[:10]
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# Wishlist functionality
def wishlist(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to view your wishlist.")
        return redirect('login')
    
    # Get wishlist from session (placeholder - should be in database)
    wishlist_items = request.session.get('wishlist', [])
    books = Book.objects.filter(id__in=wishlist_items).select_related('store')
    
    context = {
        'wishlist_books': books,
        'wishlist_count': len(wishlist_items),
    }
    
    return render(request, 'customer/wishlist.html', context)

def add_to_wishlist(request, book_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to add to wishlist.")
        return redirect('login')
    
    book = get_object_or_404(Book, id=book_id)
    
    # Initialize wishlist in session
    if 'wishlist' not in request.session:
        request.session['wishlist'] = []
    
    wishlist = request.session['wishlist']
    
    if book_id not in wishlist:
        wishlist.append(book_id)
        request.session.modified = True
        messages.success(request, f"Added '{book.title}' to your wishlist!")
    else:
        messages.info(request, f"'{book.title}' is already in your wishlist.")
    
    return redirect('book_detail', book_id=book_id)

def remove_from_wishlist(request, book_id):
    if 'wishlist' in request.session:
        wishlist = request.session['wishlist']
        if book_id in wishlist:
            wishlist.remove(book_id)
            request.session.modified = True
            messages.success(request, "Removed from wishlist.")
    
    return redirect('wishlist')

# Customer profile
def customer_profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to view your profile.")
        return redirect('login')
    
    # Get user's orders (placeholder)
    orders = []
    
    context = {
        'user': request.user,
        'orders': orders,
    }
    
    return render(request, 'customer/profile.html', context)

# Order history
def order_history(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to view your orders.")
        return redirect('login')
    
    # Mock orders for demonstration
    orders = [
        {
            'id': 'ORD-1001',
            'date': datetime.now() - timedelta(days=5),
            'items': 3,
            'total': 45.50,
            'status': 'Delivered',
            'type': 'Purchase',
        },
        {
            'id': 'ORD-1002',
            'date': datetime.now() - timedelta(days=15),
            'items': 2,
            'total': 12.00,
            'status': 'Rented',
            'type': 'Rental',
        },
    ]
    
    context = {
        'orders': orders,
        'active_rentals': [orders[1]] if len(orders) > 1 else [],
        'past_orders': [orders[0]] if orders else [],
    }
    
    return render(request, 'customer/order_history.html', context)

# Get cart count for AJAX
def get_cart_count(request):
    cart = request.session.get('cart', {'rental': [], 'purchase': []})
    count = len(cart['rental']) + len(cart['purchase'])
    return JsonResponse({'count': count})


# Quick Search API (for AJAX)
def quick_search(request):
    query = request.GET.get('q', '')
    query = query.strip()
    
    if query:
        books = Book.objects.filter(title__icontains=query)[:10]
        
        results = [
            {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'rental_price': str(book.rental_price),
                'sale_price': str(book.sale_price),
                'available_rent': book.available_copies > 0,
                'available_buy': book.available_sales > 0,
                'url': f"/book/{book.id}/"
            }
            for book in books
        ]
    else:
        results = []
    
    return JsonResponse({'results': results})
