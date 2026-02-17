from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
import json
from decimal import Decimal
from django.contrib.auth.models import User, Group
from .models import Features, Store, Book, Order, OrderItem, Delivery, CustomerReview, Wishlist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from datetime import datetime, timedelta
from django.db.models import Sum, Q, Count
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


def get_managed_stores(user):
    if not user.is_authenticated:
        return Store.objects.none()

    if user.is_superuser or user.is_staff or user.username.lower() in ('admin', 'administrator'):
        return Store.objects.all()

    name_candidates = {user.username}
    full_name = user.get_full_name().strip()
    if full_name:
        name_candidates.add(full_name)

    store_filter = Q()
    has_filter = False
    for candidate in name_candidates:
        value = (candidate or '').strip()
        if not value:
            continue
        has_filter = True
        store_filter |= Q(owner_full_name__iexact=value)

    if user.email:
        has_filter = True
        store_filter |= Q(email__iexact=user.email.strip())

    return Store.objects.filter(store_filter).distinct() if has_filter else Store.objects.none()


def can_manage_order(user, order):
    if not user.is_authenticated or get_account_type(user) != STORE_OWNER_GROUP:
        return False
    if user.is_superuser:
        return True
    return get_managed_stores(user).filter(id=order.store_id).exists()


STORE_OWNER_GROUP = "store_owner"
CUSTOMER_GROUP = "customer"
VALID_ACCOUNT_TYPES = {STORE_OWNER_GROUP, CUSTOMER_GROUP}


def get_account_type(user):
    if user.is_superuser:
        return STORE_OWNER_GROUP
    if user.groups.filter(name=STORE_OWNER_GROUP).exists():
        return STORE_OWNER_GROUP
    if user.groups.filter(name=CUSTOMER_GROUP).exists():
        return CUSTOMER_GROUP
    if user.is_authenticated and get_managed_stores(user).exists():
        return STORE_OWNER_GROUP
    return CUSTOMER_GROUP


def ensure_store_owner(request):
    if get_account_type(request.user) != STORE_OWNER_GROUP:
        messages.error(request, "This page is only available for store owners.")
        if request.user.is_authenticated:
            return redirect('customer_dashboard')
        return redirect('login')
    return None


def index(request):
    feature = Features.objects.all()
    return render(request, 'index.html', {'features': feature})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        account_type = request.POST.get("account_type", CUSTOMER_GROUP)

        if account_type not in VALID_ACCOUNT_TYPES:
            messages.info(request, "Please select a valid account type")
            return redirect('register')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                role_group, _ = Group.objects.get_or_create(name=account_type)
                user.groups.add(role_group)
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
            if get_account_type(user) == STORE_OWNER_GROUP:
                return redirect('store_dashboard')
            return redirect('customer_dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, "login.html")


def logout(request):
    auth_logout(request)
    return redirect('login')


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



def store_list(request):
    # Only show stores that have at least one book
    stores = Store.objects.filter(book__isnull=False).distinct()

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
        'cities': Store.objects.filter(book__isnull=False).values_list('city', flat=True).distinct(),
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









@login_required
def store_dashboard(request):
    # Get stores owned by the user
    stores = Store.objects.filter(owner_full_name=request.user.username)
    
    # Get orders for these stores
    orders = Order.objects.filter(store__in=stores)
    
    # Calculate metrics
    total_orders = orders.count()
    pending_orders_count = orders.filter(status='pending').count()  # For badge
    active_rentals = orders.filter(order_type='rent').exclude(status__in=['completed', 'cancelled']).count()
    pending_deliveries = orders.filter(delivery_option='delivery', status__in=['preparing', 'ready', 'out_for_delivery']).count()
    
    # Revenue calculations
    today = datetime.now().date()
    revenue_today = orders.filter(
        created_at__date=today,
        status__in=['delivered', 'completed']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Inventory Stats
    books = Book.objects.filter(store__in=stores)
    total_books = books.count()
    low_stock_books = books.filter(Q(available_copies__lt=5) | Q(available_sales__lt=5)).count()
    
    # Recent orders
    recent_orders = orders.order_by('-created_at')[:5]
    
    # Get wishlist count for badge
    from django.db.models import Count
    wishlist_count = 0
    if stores.exists():
        wishlist_count = Wishlist.objects.filter(book__store__in=stores).count()
    
    context = {
        'page_title': 'Store Dashboard',
        'pending_orders_count': pending_orders_count,  # For sidebar badge
        'wishlist_count': wishlist_count,  # For sidebar badge
        'store_metrics': {
            'revenue_today': revenue_today,
            'revenue_week': orders.filter(created_at__date__gte=today - timedelta(days=7), status__in=['delivered', 'completed']).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'revenue_month': orders.filter(created_at__date__gte=today.replace(day=1), status__in=['delivered', 'completed']).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'revenue_total': orders.filter(status__in=['delivered', 'completed']).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'active_rentals': active_rentals,
            'pending_deliveries': pending_deliveries,
            'pending_orders': pending_orders_count,
            'total_books': total_books,
            'low_stock_books': low_stock_books,
            'new_customers': orders.values('customer').distinct().count(),
        },
        'recent_orders': recent_orders,
    }
    return render(request, 'store/dashboard.html', context)




@login_required
def add_book(request):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    if request.method == 'POST':
        messages.success(request, 'Book added (stub).')
        return redirect('store_dashboard')
    return render(request, "store/add_book.html")


@login_required
def view_inventory(request):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    books = Book.objects.filter(store__in=get_managed_stores(request.user)).order_by('-created_at')
    return render(request, 'store/view_inventory.html', {'books': books})
'''

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

    return render(request, "store/add_book.html")   '''
        


@login_required
def add_book_registration(request):
    guard = ensure_store_owner(request)
    if guard:
        return guard

    managed_stores = get_managed_stores(request.user).order_by('id')
    if not managed_stores.exists():
        messages.warning(request, "You don't have an assigned store yet.")
        return redirect('store_registration')

    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        genre = request.POST.get("genre")
        publication_year = request.POST.get("publication_year")
        total_copies = int(request.POST.get("total_copies") or 0)
        available_copies = int((request.POST.get("available_copies") or request.POST.get("available_rent") or 0))
        available_sales = int((request.POST.get("available_sales") or request.POST.get("available_sale") or 0))
        rental_price = float(request.POST.get("rental_price") or 0)
        sale_price = float(request.POST.get("sale_price") or 0)

        selected_store_id = request.POST.get("store_id")
        if selected_store_id:
            store = managed_stores.filter(id=selected_store_id).first()
            if not store:
                messages.error(request, "Invalid store selected.")
                return redirect('add_book_registration')
        else:
            store = managed_stores.first()

        if title and author:
            # Check for existing book in this store
            existing_book = Book.objects.filter(title=title, author=author, store=store).first()
            if existing_book:
                # Update existing book
                existing_book.total_copies = total_copies
                existing_book.available_copies = available_copies
                existing_book.available_sales = available_sales
                existing_book.rental_price = rental_price
                existing_book.sale_price = sale_price
                existing_book.save()
                messages.info(request, f"Book updated successfully in {store.store_name}.")
            else:
                # Create new book with store
                Book.objects.create(
                    title=title,
                    author=author,
                    genre=genre,
                    publication_year=publication_year or None,
                    total_copies=total_copies,
                    available_copies=available_copies,
                    available_sales=available_sales,
                    rental_price=rental_price,
                    sale_price=sale_price,
                    store=store,  # This is crucial!
                )
                messages.success(request, f"Book added successfully to {store.store_name}!")
             
            return redirect('add_book_registration')

        messages.info(request, "Title and Author are required")
        return redirect('add_book')

    return render(request, "store/add_book.html")























'''

        
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



'''




@login_required
def edit_book(request, id):
    guard = ensure_store_owner(request)
    if guard:
        return guard

    managed_stores = get_managed_stores(request.user)
    book = get_object_or_404(Book, pk=id, store__in=managed_stores)
    
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        genre = request.POST.get("genre")
        publication_year = request.POST.get("publication_year")
        total_copies = int(request.POST.get("total_copies") or 0)
        available_copies = int((request.POST.get("available_copies") or request.POST.get("available_rent") or 0))
        available_sales = int((request.POST.get("available_sales") or request.POST.get("available_sale") or 0))
        rental_price = float(request.POST.get("rental_price") or 0)
        sale_price = float(request.POST.get("sale_price") or 0)
        
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
        # Store remains the same, don't change it
        
        book.save()
        messages.success(request, "Book updated successfully.")
        return redirect('view_inventory')
    
    return render(request, 'store/edit_book.html', {'book': book})




#store registration view and edit   and  delete


@login_required
def store_registration_view(request):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    stores = get_managed_stores(request.user)
    return render(request, 'store/registration/registration_view.html', {'stores': stores})


@login_required
def edit_store(request, id):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    try:
        store = get_managed_stores(request.user).get(pk=id)
    except Store.DoesNotExist:
        messages.error(request, "Store not found or not assigned to your account.")
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










































@login_required
def delete_store(request, id):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    try:
        store = get_managed_stores(request.user).get(pk=id)
    except Store.DoesNotExist:
        messages.error(request, "Store not found or not assigned to your account.")
        return redirect('store_registration_view')

    store.delete()
    messages.success(request, "Store deleted.")
    return redirect('store_registration_view')






























@login_required
def book_delete(request, id):
    guard = ensure_store_owner(request)
    if guard:
        return guard

    managed_stores = get_managed_stores(request.user)
    book = get_object_or_404(Book, pk=id, store__in=managed_stores)
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('view_inventory')

    book.delete()
    messages.success(request, "Book deleted successfully.")
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
                    available_copies=ab.available_copies or 0,  # This is correct
                    available_sales=ab.available_sales or 0,    # This is correct
                    rental_price=ab.rental_price or 0,
                    sale_price=ab.sale_price or 0,
                    store=ab.store if hasattr(ab, 'store') else None,
                )
        
    except Exception as e:
        print(f"Error syncing books: {e}")
        # Fall back silently if migration step fails for any reason
        pass

        # Get all books
        books = Book.objects.select_related('store').filter(store__isnull=False)
    
    # Debug: Print first few books
    print("\n=== DEBUG: First 5 Books ===")
    for book in books[:5]:
        print(f"Book: {book.title}")
        print(f"  Available Copies (rent): {book.available_copies}")
        print(f"  Available Sales (purchase): {book.available_sales}")
        print(f"  Total Copies: {book.total_copies}")
    print("=== END DEBUG ===\n")
    
    # ... rest of your existing code ...
















    # Get distinct genres for filtering
    genres = Book.objects.values_list('genre', flat=True).distinct()
    
    # Get all stores for filtering
    stores = Store.objects.all()
    
    # Search functionality (title only)
    search_query = request.GET.get('search', '')
    if search_query:
        search_query = search_query.strip()
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
    
    # Get total count before pagination
    total_books = books.count()
    
    # Debug info
    debug_count = total_books
    debug_titles = list(books.values_list('title', flat=True)[:5])
    
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
        'total_books': total_books,
        'debug_count': debug_count,
        'debug_titles': debug_titles,
        'paginator': paginator,
    }
    
    return render(request, 'customer/dashboard.html', context)















def book_detail(request, book_id):
    # IMPORTANT: Only get books that have a store
    book = get_object_or_404(
        Book.objects.select_related('store').filter(store__isnull=False), 
        id=book_id
    )
    
    # Get similar books (same genre, with stores)
    similar_books = Book.objects.filter(
        genre=book.genre,
        store__isnull=False
    ).exclude(id=book_id).select_related('store')[:4]
    
    # Check if user can rent or buy
    can_rent = book.available_copies > 0 and book.store is not None
    can_buy = book.available_sales > 0 and book.store is not None
    
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
                try:
                    hours = f"{open_time.strftime('%I:%M %p')} - {close_time.strftime('%I:%M %p')}"
                except:
                    hours = f"{open_time} - {close_time}"
                opening_hours.append({
                    'day': day_display,
                    'hours': hours
                })
            elif is_open:
                opening_hours.append({
                    'day': day_display,
                    'hours': "Open"
                })
    
    # Check if book is in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, book=book).exists()
    
    # Get cart count
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.session.get('cart', {'rental': [], 'purchase': []})
        cart_count = len(cart['rental']) + len(cart['purchase'])
    
    context = {
        'book': book,
        'similar_books': similar_books,
        'can_rent': can_rent,
        'can_buy': can_buy,
        'store': store,
        'opening_hours': opening_hours,
        'in_wishlist': in_wishlist,
        'cart_count': cart_count,
    }
    
    return render(request, 'customer/book_detail.html', context)



# Shopping Cart with session management
@login_required
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
        'checkout_url': reverse('checkout'),
        'checkout_login_url': f"{reverse('login')}?next={reverse('checkout')}",
    }
    
    return render(request, 'customer/cart.html', context)

@login_required
def add_to_cart_rent(request, book_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to add items to cart.")
        return redirect('login')
    
    try:
        book = Book.objects.select_related('store').get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('customer_dashboard')

    # Check if book has a store
    if not book.store:
        messages.error(request, 
            "This book is not associated with any store. "
            "Please contact the store owner to fix this issue."
        )
        return redirect('book_detail', book_id=book_id)

    # Check if store is active and offers rental
    if not book.store.offers_rental:
        messages.error(request, 
            f"'{book.store.store_name}' does not offer rental services for this book."
        )
        return redirect('book_detail', book_id=book_id)

    # Check availability
    if book.available_copies <= 0:
        messages.error(request, 
            f"'{book.title}' is currently out of stock for rent. "
            f"Available copies: {book.available_copies}"
        )
        return redirect('book_detail', book_id=book_id)
    
    # Initialize cart in session if not exists
    if 'cart' not in request.session:
        request.session['cart'] = {'rental': [], 'purchase': []}
    
    cart = request.session['cart']
    
    # Check if already in cart
    if book_id not in cart['rental']:
        cart['rental'].append(book_id)
        request.session.modified = True
        messages.success(request, 
            f"✅ Added '{book.title}' to your rental cart from {book.store.store_name}!"
        )
    else:
        messages.info(request, f"'{book.title}' is already in your rental cart.")
    
    return redirect('book_detail', book_id=book_id)


@login_required
def add_to_cart_buy(request, book_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to add items to cart.")
        return redirect('login')
    
    try:
        book = Book.objects.select_related('store').get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('customer_dashboard')

    # Check if book has a store
    if not book.store:
        messages.error(request, 
            "This book is not associated with any store. "
            "Please contact the store owner to fix this issue."
        )
        return redirect('book_detail', book_id=book_id)

    # Check if store offers sale
    if not book.store.offers_sale:
        messages.error(request, 
            f"'{book.store.store_name}' does not offer purchase services for this book."
        )
        return redirect('book_detail', book_id=book_id)

    # Check availability
    if book.available_sales <= 0:
        messages.error(request, 
            f"'{book.title}' is currently out of stock for purchase. "
            f"Available copies: {book.available_sales}"
        )
        return redirect('book_detail', book_id=book_id)
    
    # Initialize cart in session if not exists
    if 'cart' not in request.session:
        request.session['cart'] = {'rental': [], 'purchase': []}
    
    cart = request.session['cart']
    
    # Check if already in cart
    if book_id not in cart['purchase']:
        cart['purchase'].append(book_id)
        request.session.modified = True
        messages.success(request, 
            f"✅ Added '{book.title}' to your purchase cart from {book.store.store_name}!"
        )
    else:
        messages.info(request, f"'{book.title}' is already in your purchase cart.")
    
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
@login_required
def wishlist(request):
    # Get wishlist items from database
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('book', 'book__store')
    
    # Extract books from wishlist items
    books = [item.book for item in wishlist_items]
    
    context = {
        'wishlist_books': books,
        'wishlist_count': len(books),
    }
    
    return render(request, 'customer/wishlist.html', context)

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if already in wishlist
    if Wishlist.objects.filter(user=request.user, book=book).exists():
        messages.info(request, f"'{book.title}' is already in your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, book=book)
        messages.success(request, f"Added '{book.title}' to your wishlist!")
    
    return redirect('book_detail', book_id=book_id)

@login_required
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Wishlist.objects.filter(user=request.user, book=book).delete()
    messages.success(request, "Removed from wishlist.")
    return redirect('wishlist')

@login_required
def clear_wishlist(request):
    Wishlist.objects.filter(user=request.user).delete()
    messages.success(request, "Wishlist cleared.")
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













@login_required
def create_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    cart = request.session.get('cart', {'rental': [], 'purchase': []})
    if not cart['rental'] and not cart['purchase']:
        messages.error(request, 'Your cart is empty')
        return redirect('shopping_cart')

    payload = request.POST
    if request.content_type and request.content_type.startswith('application/json'):
        try:
            payload = json.loads(request.body.decode('utf-8') or '{}')
        except (json.JSONDecodeError, UnicodeDecodeError):
            messages.error(request, 'Invalid checkout payload.')
            return redirect('checkout')

    get_value = payload.get if hasattr(payload, 'get') else lambda key, default='': default

    delivery_option = get_value('delivery_option', 'pickup')
    if delivery_option not in ('pickup', 'delivery'):
        delivery_option = 'pickup'

    delivery_address = (get_value('delivery_address', '') or '').strip()
    preferred_time = get_value('preferred_time', '')
    notes = get_value('notes', '')

    try:
        delivery_fee = Decimal(str(get_value('delivery_fee', '0') or '0'))
    except Exception:
        delivery_fee = Decimal('0')

    try:
        rental_days = int(get_value('rental_days', 7))
    except (TypeError, ValueError):
        rental_days = 7
    rental_days = max(rental_days, 1)

    if delivery_option == 'delivery' and not delivery_address:
        messages.error(request, 'Delivery address is required for delivery orders.')
        return redirect('checkout')

    try:
        created_orders = []
        with transaction.atomic():
            rental_items = list(
                Book.objects.select_for_update().filter(id__in=cart.get('rental', []), store__isnull=False)
            )
            purchase_items = list(
                Book.objects.select_for_update().filter(id__in=cart.get('purchase', []), store__isnull=False)
            )

            all_items = rental_items + purchase_items
            if not all_items:
                messages.error(request, 'No valid items in cart')
                return redirect('shopping_cart')

            rental_ids = {book.id for book in rental_items}
            purchase_ids = {book.id for book in purchase_items}
            missing_rental_ids = [book_id for book_id in cart.get('rental', []) if book_id not in rental_ids]
            missing_purchase_ids = [book_id for book_id in cart.get('purchase', []) if book_id not in purchase_ids]

            if missing_rental_ids or missing_purchase_ids:
                messages.error(request, 'Some books are no longer available. Please review your cart.')
                return redirect('shopping_cart')

            items_by_store = {}
            for item in rental_items:
                store_group = items_by_store.setdefault(item.store_id, {'store': item.store, 'rental': [], 'purchase': []})
                store_group['rental'].append(item)

            for item in purchase_items:
                store_group = items_by_store.setdefault(item.store_id, {'store': item.store, 'rental': [], 'purchase': []})
                store_group['purchase'].append(item)

            unavailable_titles = []
            for item in rental_items:
                if item.available_copies < 1:
                    unavailable_titles.append(item.title)
            for item in purchase_items:
                if item.available_sales < 1:
                    unavailable_titles.append(item.title)

            if unavailable_titles:
                messages.error(
                    request,
                    'Not enough stock for: ' + ', '.join(sorted(set(unavailable_titles)))
                )
                return redirect('shopping_cart')

            for group in items_by_store.values():
                store = group['store']
                store_rentals = group['rental']
                store_purchases = group['purchase']

                total_amount = Decimal('0')
                for item in store_rentals:
                    total_amount += Decimal(str(item.rental_price)) * Decimal(str(rental_days))
                for item in store_purchases:
                    total_amount += Decimal(str(item.sale_price))
                if delivery_option == 'delivery':
                    total_amount += delivery_fee

                if store_rentals and store_purchases:
                    order_type = 'mixed'
                elif store_rentals:
                    order_type = 'rent'
                else:
                    order_type = 'buy'

                order = Order.objects.create(
                    customer=request.user,
                    order_number='',
                    order_type=order_type,
                    store=store,
                    total_amount=total_amount,
                    status='pending',
                    payment_method='cash',
                    payment_status='pending',
                    delivery_option=delivery_option,
                    delivery_address=delivery_address if delivery_option == 'delivery' else '',
                    preferred_time=preferred_time,
                    delivery_fee=delivery_fee if delivery_option == 'delivery' else Decimal('0'),
                    rental_days=rental_days if store_rentals else None,
                    notes=notes,
                )

                for item in store_rentals:
                    OrderItem.objects.create(
                        order=order,
                        book=item,
                        quantity=1,
                        price=Decimal(str(item.rental_price)) * Decimal(str(rental_days)),
                        rental_days=rental_days,
                        item_type='rent',
                    )
                    item.available_copies -= 1
                    item.save(update_fields=['available_copies'])

                for item in store_purchases:
                    OrderItem.objects.create(
                        order=order,
                        book=item,
                        quantity=1,
                        price=Decimal(str(item.sale_price)),
                        item_type='buy',
                    )
                    item.available_sales -= 1
                    item.save(update_fields=['available_sales'])

                created_orders.append(order)

            request.session['cart'] = {'rental': [], 'purchase': []}
            request.session.modified = True

        messages.success(request, 'Order placed successfully! Waiting for store approval.')
        if created_orders:
            return redirect('order_detail', order_id=created_orders[0].id)
        return redirect('order_history')
    except Exception as e:
        messages.error(request, f'Error creating order: {str(e)}')
        return redirect('checkout')






















@login_required
def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to checkout.")
        return redirect('login')
    
    cart = request.session.get('cart', {'rental': [], 'purchase': []})

    if not cart['rental'] and not cart['purchase']:
        messages.warning(request, "Your cart is empty.")
        return redirect('customer_dashboard')

    # Load cart items and remove any that lack a store
    rental_items_qs = Book.objects.filter(id__in=cart['rental'])
    purchase_items_qs = Book.objects.filter(id__in=cart['purchase'])

    removed_titles = []
    rental_items = []
    for b in rental_items_qs:
        if b.store:
            rental_items.append(b)
        else:
            removed_titles.append(b.title)

    purchase_items = []
    for b in purchase_items_qs:
        if b.store:
            purchase_items.append(b)
        else:
            removed_titles.append(b.title)

    if removed_titles:
        # Remove invalid ids from session cart
        cart['rental'] = [i for i in cart.get('rental', []) if Book.objects.filter(id=i, store__isnull=False).exists()]
        cart['purchase'] = [i for i in cart.get('purchase', []) if Book.objects.filter(id=i, store__isnull=False).exists()]
        request.session['cart'] = cart
        request.session.modified = True
        messages.warning(request, 'Some items were removed from your cart because they are not available in any store: ' + ', '.join(removed_titles))
    
    # Calculate totals
    rental_total = sum(float(item.rental_price) for item in rental_items)
    purchase_total = sum(float(item.sale_price) for item in purchase_items)
    total = rental_total + purchase_total
    
    # Get default rental days
    default_rental_days = 7
    
    context = {
        'rental_items': rental_items,
        'purchase_items': purchase_items,
        'rental_total': rental_total,
        'purchase_total': purchase_total,
        'total': total,
        'default_rental_days': default_rental_days,
    }
    
    return render(request, 'customer/checkout.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    items = order.items.all()
    delivery_fee = order.delivery_fee or Decimal('0')
    subtotal = (order.total_amount or Decimal('0')) - delivery_fee
    
    # Check if delivery exists
    try:
        delivery = Delivery.objects.get(order=order)
    except Delivery.DoesNotExist:
        delivery = None
    
    context = {
        'order': order,
        'items': items,
        'delivery': delivery,
        'subtotal': subtotal,
    }
    
    return render(request, 'customer/order_detail.html', context)


@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    try:
        delivery = Delivery.objects.get(order=order)
    except Delivery.DoesNotExist:
        delivery = None
    
    context = {
        'order': order,
        'delivery': delivery,
    }
    
    return render(request, 'customer/track_order.html', context)


@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)
    
    # Filter by time
    time_filter = request.GET.get('time', 'all')
    if time_filter == '30days':
        thirty_days_ago = datetime.now() - timedelta(days=30)
        orders = orders.filter(created_at__gte=thirty_days_ago)
    elif time_filter == '7days':
        seven_days_ago = datetime.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=seven_days_ago)
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'time_filter': time_filter,
    }
    
    return render(request, 'customer/order_history.html', context)


@login_required
def mark_order_finished(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('order_detail', order_id=order.id)

    if order.status == 'delivered':
        order.status = 'completed'
        order.save()
        messages.success(request, f"Order #{order.order_number} marked as completed.")
    elif order.status == 'completed':
        messages.info(request, f"Order #{order.order_number} is already completed.")
    else:
        messages.warning(request, "You can finish an order only after it is delivered.")

    return redirect('customer_order_history')


# Store Owner Views
@login_required
def store_orders(request):
    # Get stores owned by the user
    stores = get_managed_stores(request.user)
    if not stores.exists():
        messages.info(request, "No store assigned to this account yet. Showing empty order management.")
    
    if not stores.exists():
        messages.warning(request, "You don't own any stores yet.")
        return redirect('store_dashboard')
    
    # Get orders for these stores
    orders = Order.objects.filter(store__in=stores).order_by('-created_at')
    
    # Get pending orders count for sidebar badge
    pending_orders_count = orders.filter(status='pending').count()
    
    # Calculate statistics
    total_orders = orders.count()
    total_revenue = orders.filter(status__in=['delivered', 'completed']).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Today's revenue
    today = datetime.now().date()
    today_revenue = orders.filter(
        created_at__date=today, 
        status__in=['delivered', 'completed']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Counts for different statuses
    pending_count = orders.filter(status='pending').count()
    preparing_count = orders.filter(status='preparing').count()
    ready_count = orders.filter(status='ready').count()
    out_for_delivery_count = orders.filter(status='out_for_delivery').count()
    delivered_count = orders.filter(status='delivered').count()
    completed_count = orders.filter(status='completed').count()
    cancelled_count = orders.filter(status='cancelled').count()
    
    # Apply filters
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)
    
    order_type_filter = request.GET.get('type', 'all')
    if order_type_filter != 'all':
        orders = orders.filter(order_type=order_type_filter)
    
    date_filter = request.GET.get('date', 'all')
    if date_filter == 'today':
        orders = orders.filter(created_at__date=today)
    elif date_filter == 'week':
        week_ago = datetime.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = datetime.now() - timedelta(days=30)
        orders = orders.filter(created_at__gte=month_ago)
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page', 1)
    
    try:
        orders_page = paginator.page(page_number)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)
    
    # Get wishlist count for sidebar badge
    wishlist_count = Wishlist.objects.filter(book__store__in=stores).count()
    
    context = {
        'orders': orders_page,
        'stores': stores,
        'status_filter': status_filter,
        'order_type_filter': order_type_filter,
        'date_filter': date_filter,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'month_revenue': orders.filter(
            created_at__date__gte=today.replace(day=1),
            status__in=['delivered', 'completed']
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'pending_orders': pending_count,
        'preparing_orders': preparing_count,
        'ready_orders': ready_count,
        'out_for_delivery_orders': out_for_delivery_count,
        'delivered_orders': delivered_count,
        'completed_orders': completed_count,
        'cancelled_orders': cancelled_count,
        'active_orders': preparing_count + ready_count + out_for_delivery_count,
        'pending_orders_count': pending_orders_count,  # For sidebar badge
        'wishlist_count': wishlist_count,  # For sidebar badge
    }
    
    return render(request, 'store/order_management.html', context)
   # return render(request, 'customer/order_history.html', context)





@login_required
def process_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user owns the store
    if not can_manage_order(request.user, order):
        messages.error(request, "You don't have permission to access this order.")
        return redirect('store_orders')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Approve order
        if action == 'approve':
            if order.status != 'pending':
                messages.warning(request, f"Order #{order.order_number} is not pending approval.")
                return redirect('process_order', order_id=order_id)
            order.status = 'approved'
            order.save()
            messages.success(request, f"Order #{order.order_number} has been approved.")
            return redirect('store_order_history')
        
        # Reject order
        elif action == 'reject':
            if order.status == 'cancelled':
                messages.info(request, f"Order #{order.order_number} is already declined.")
                return redirect('process_order', order_id=order_id)
            if order.status != 'pending':
                messages.warning(request, f"Order #{order.order_number} can only be declined while pending.")
                return redirect('process_order', order_id=order_id)

            reason = request.POST.get('rejection_reason', 'No reason provided')
            
            # Restore stock
            for item in order.items.all():
                book = item.book
                if item.item_type == 'rent':
                    book.available_copies += item.quantity
                elif item.item_type == 'buy':
                    book.available_sales += item.quantity
                book.save()
            
            order.status = 'cancelled'
            order.store_notes = f"Declined on {datetime.now().strftime('%Y-%m-%d %H:%M')}: {reason}\n\n{order.store_notes or ''}"
            order.save()
            messages.warning(request, f"Order #{order.order_number} has been declined.")
            return redirect('store_order_history')
        
        # Update status
        elif action == 'update_status':
            new_status = request.POST.get('status')
            allowed_statuses = {status for status, _ in Order.ORDER_STATUS_CHOICES}
            if new_status not in allowed_statuses:
                messages.error(request, "Invalid status selected.")
                return redirect('process_order', order_id=order_id)
            order.status = new_status
            order.save()
            
            # Create delivery tracking if out for delivery
            if new_status == 'out_for_delivery' and order.delivery_option == 'delivery':
                delivery, created = Delivery.objects.get_or_create(order=order)
                if created:
                    delivery.status = 'assigned'
                    delivery.save()
            
            messages.success(request, f"Order status updated to {order.get_status_display()}")
        
        # Update delivery info
        elif action == 'update_delivery':
            driver_name = request.POST.get('driver_name')
            driver_phone = request.POST.get('driver_phone')
            estimated_arrival = request.POST.get('estimated_arrival')
            delivery_notes = request.POST.get('delivery_notes')
            
            delivery, created = Delivery.objects.get_or_create(order=order)
            delivery.driver_name = driver_name
            delivery.driver_phone = driver_phone
            if estimated_arrival:
                try:
                    delivery.estimated_arrival = datetime.fromisoformat(estimated_arrival)
                except:
                    pass
            delivery.delivery_notes = delivery_notes
            delivery.save()
            
            messages.success(request, "Delivery information updated")
        
        # Add note
        elif action == 'add_note':
            note = request.POST.get('store_note')
            if note:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                if order.store_notes:
                    order.store_notes += f"\n{timestamp}: {note}"
                else:
                    order.store_notes = f"{timestamp}: {note}"
                order.save()
                messages.success(request, "Note added")
        
        return redirect('process_order', order_id=order_id)
    
    # GET request - show order processing page
    items = order.items.all()
    
    # Get delivery info if exists
    try:
        delivery = Delivery.objects.get(order=order)
    except Delivery.DoesNotExist:
        delivery = None
    
    # Create a simple timeline
    order_status_timeline = [
        {'status': 'Order Placed', 'time': order.created_at.strftime('%b %d, %Y %I:%M %p')},
    ]
    
    if order.status != 'pending':
        order_status_timeline.append({'status': 'Store Approved', 'time': order.updated_at.strftime('%b %d, %Y %I:%M %p')})
    
    context = {
        'order': order,
        'items': items,
        'delivery': delivery,
        'order_status_timeline': order_status_timeline,
    }
    
    return render(request, 'store/process_order.html', context)



@login_required
def update_delivery_location(request, delivery_id):
    if request.method == 'POST':
        delivery = get_object_or_404(Delivery, id=delivery_id)
        
        # Check if user owns the store
        if not can_manage_order(request.user, delivery.order):
            return JsonResponse({'success': False, 'message': 'Permission denied'})
        
        data = json.loads(request.body)
        location = data.get('location')
        
        if location:
            delivery.current_location = location
            delivery.save()
            return JsonResponse({'success': True, 'message': 'Location updated'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def store_dashboard(request):
    guard = ensure_store_owner(request)
    if guard:
        return guard

    # Get stores owned by the user
    stores = get_managed_stores(request.user)
    if not stores.exists():
        messages.info(request, "No store is assigned to this account yet.")
    
    # Get orders for these stores
    orders = Order.objects.filter(store__in=stores)
    today = datetime.now().date()
    
    # Calculate metrics
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    active_orders = orders.filter(status__in=['approved', 'contacted', 'preparing', 'ready', 'out_for_delivery']).count()
    completed_orders = orders.filter(status='completed').count()
    cancelled_orders = orders.filter(status='cancelled').count()
    today_revenue = orders.filter(
        created_at__date=today,
        status__in=['completed', 'delivered']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    month_revenue = orders.filter(
        created_at__date__gte=today.replace(day=1),
        status__in=['completed', 'delivered']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Recent orders
    recent_orders = orders.order_by('-created_at')[:5]

    # Sidebar / dashboard support data
    books = Book.objects.filter(store__in=stores)
    primary_store = stores.first()
    account_owner = (
        primary_store.owner_full_name
        if primary_store and primary_store.owner_full_name
        else (request.user.get_full_name().strip() or request.user.username)
    )
    
    context = {
        'stores': stores,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'active_orders': active_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'revenue_today': today_revenue,  # Backward-compatible alias
        'pending_orders_count': pending_orders,
        'account_owner': account_owner,
        'store_metrics': {
            'pending_orders': pending_orders,
            'revenue_today': today_revenue,
            'revenue_month': month_revenue,
            'total_books': books.count(),
        },
        'recent_orders': recent_orders,
    }
    
    return render(request, 'store/dashboard.html', context)


@login_required
def add_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    if order.status != 'completed':
        messages.error(request, "You can only review completed orders.")
        return redirect('order_history')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Check if review already exists
        if CustomerReview.objects.filter(order=order).exists():
            messages.error(request, "You have already reviewed this order.")
            return redirect('order_history')
        
        CustomerReview.objects.create(
            customer=request.user,
            store=order.store,
            order=order,
            rating=rating,
            comment=comment
        )
        
        messages.success(request, "Thank you for your review!")
        return redirect('order_history')
    
    return render(request, 'customer/add_review.html', {'order': order})




def clear_wishlist(request):
    if 'wishlist' in request.session:
        request.session['wishlist'] = []
        request.session.modified = True
        messages.success(request, "Wishlist cleared.")
    return redirect('wishlist')







@login_required
def update_book_availability(request):
    guard = ensure_store_owner(request)
    if guard:
        return JsonResponse({'success': False, 'message': 'Store-owner access required.'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')
            total_copies = int(data.get('total_copies', 0))
            available_copies = int(data.get('available_copies', 0))
            available_sales = int(data.get('available_sales', 0))

            book = Book.objects.get(id=book_id, store__in=get_managed_stores(request.user))
            book.total_copies = total_copies
            book.available_copies = available_copies
            book.available_sales = available_sales
            book.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def manage_books(request):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    books = Book.objects.filter(store__in=get_managed_stores(request.user)).order_by('-created_at')
    return render(request, 'store/manage_books.html', {'books': books})





'''

@login_required
def store_orders(request):
    # Get stores owned by the user
    stores = get_managed_stores(request.user)
    if not stores.exists():
        messages.info(request, "No store assigned to this account yet. Showing empty order management.")
    
    # Get orders for these stores
    orders = Order.objects.filter(store__in=stores).order_by('-created_at')
    
    # Calculate statistics
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Get today's date
    today = datetime.now().date()
    today_revenue = orders.filter(created_at__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Get this week's revenue
    week_ago = datetime.now() - timedelta(days=7)
    week_revenue = orders.filter(created_at__gte=week_ago).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Get this month's revenue
    month_ago = datetime.now() - timedelta(days=30)
    month_revenue = orders.filter(created_at__gte=month_ago).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Apply filters
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)
    
    order_type_filter = request.GET.get('type', 'all')
    if order_type_filter != 'all':
        orders = orders.filter(order_type=order_type_filter)
    
    date_filter = request.GET.get('date', 'all')
    if date_filter == 'today':
        orders = orders.filter(created_at__date=today)
    elif date_filter == 'week':
        orders = orders.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        orders = orders.filter(created_at__gte=month_ago)
    
    # Count pending orders
    pending_orders = orders.filter(status__in=['pending', 'contacted', 'preparing']).count()
    
    # Count rental orders
    rental_orders = orders.filter(order_type='rent', status__in=['pending', 'preparing', 'ready', 'out_for_delivery']).count()
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page', 1)
    
    try:
        orders_page = paginator.page(page_number)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)
    
    context = {
        'orders': orders_page,
        'stores': stores,
        'status_filter': status_filter,
        'order_type_filter': order_type_filter,
        'date_filter': date_filter,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'week_revenue': week_revenue,
        'month_revenue': month_revenue,
        'pending_orders': pending_orders,
        'rental_orders': rental_orders,
    }
    
    return render(request, 'store/order_history.html', context)


'''

def _build_store_orders_context(request):
    # Get stores owned by the user
    stores = get_managed_stores(request.user)
    if not stores.exists():
        messages.info(request, "No store assigned to this account yet. Showing empty order management.")

    # Get orders for these stores
    orders = Order.objects.filter(store__in=stores).order_by('-created_at')

    # Get pending orders count for sidebar badge
    pending_orders_count = orders.filter(status='pending').count()

    # Apply filters
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    order_type_filter = request.GET.get('type', 'all')
    if order_type_filter != 'all':
        orders = orders.filter(order_type=order_type_filter)

    date_filter = request.GET.get('date', 'all')
    today = datetime.now().date()

    if date_filter == 'today':
        orders = orders.filter(created_at__date=today)
    elif date_filter == 'week':
        week_ago = datetime.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = datetime.now() - timedelta(days=30)
        orders = orders.filter(created_at__gte=month_ago)

    # Calculate statistics
    total_orders = orders.count()

    # Pending orders (waiting for approval)
    pending_count = orders.filter(status='pending').count()
    approved_count = orders.filter(status='approved').count()
    preparing_count = orders.filter(status='preparing').count()
    ready_count = orders.filter(status='ready').count()
    out_for_delivery_count = orders.filter(status='out_for_delivery').count()
    completed_count = orders.filter(status='completed').count()
    cancelled_count = orders.filter(status='cancelled').count()
    rental_orders = orders.filter(order_type='rent', status__in=['pending', 'approved', 'preparing', 'ready', 'out_for_delivery']).count()

    # Revenue calculations
    total_revenue = orders.filter(status__in=['delivered', 'completed']).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    today_revenue = orders.filter(created_at__date=today, status__in=['delivered', 'completed']).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    week_revenue = orders.filter(created_at__date__gte=today - timedelta(days=7), status__in=['delivered', 'completed']).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    month_revenue = orders.filter(
        created_at__date__gte=today.replace(day=1),
        status__in=['delivered', 'completed'],
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page', 1)

    try:
        orders_page = paginator.page(page_number)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)

    # Get wishlist count for sidebar badge
    wishlist_count = Wishlist.objects.filter(book__store__in=stores).count()

    return {
        'orders': orders_page,
        'stores': stores,
        'status_filter': status_filter,
        'order_type_filter': order_type_filter,
        'date_filter': date_filter,
        'total_orders': total_orders,
        'pending_orders': pending_count,
        'active_orders': approved_count + preparing_count + ready_count + out_for_delivery_count,
        'completed_orders': completed_count,
        'cancelled_orders': cancelled_count,
        'rental_orders': rental_orders,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'week_revenue': week_revenue,
        'month_revenue': month_revenue,
        'pending_orders_count': pending_orders_count,  # For sidebar badge
        'wishlist_count': wishlist_count,  # For sidebar badge
    }


@login_required
def store_orders(request):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    context = _build_store_orders_context(request)
    return render(request, 'store/order_management.html', context)


@login_required
def store_order_history(request):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    context = _build_store_orders_context(request)
    return render(request, 'store/order_history.html', context)






@login_required
def store_order_detail(request, order_id):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user owns the store
    if not can_manage_order(request.user, order):
        messages.error(request, "You don't have permission to access this order.")
        return redirect('store_orders')
    
    items = order.items.all()
    delivery_fee = order.delivery_fee or Decimal('0')
    subtotal = (order.total_amount or Decimal('0')) - delivery_fee
    
    # Check if delivery exists
    try:
        delivery = Delivery.objects.get(order=order)
    except Delivery.DoesNotExist:
        delivery = None
    
    context = {
        'order': order,
        'items': items,
        'delivery': delivery,
        'subtotal': subtotal,
    }
    
    return render(request, 'store/order_detail.html', context)

















@login_required
def store_wishlist(request):
    guard = ensure_store_owner(request)
    if guard:
        return guard
    # Get stores owned by the user
    stores = get_managed_stores(request.user)
    if not stores.exists():
        messages.info(request, "No store assigned to this account yet. Showing empty wishlist analytics.")
    
    # Get books from these stores and annotate with wishlist count
    books = Book.objects.filter(store__in=stores).annotate(
        wishlist_count=Count('wishlist')
    ).order_by('-wishlist_count')
    
    # Filter for "wishlisted" books (count > 0)
    wishlisted_books = books.filter(wishlist_count__gt=0)
    
    # Identify low stock books
    low_stock_books = books.filter(
        Q(available_copies__lte=2) | 
        Q(available_sales__lte=2)
    )
    
    # Calculate estimated revenue potential from wishlisted items
    estimated_revenue = 0
    for book in wishlisted_books:
        # Use rental price as base for estimation if sale price is 0
        price = book.sale_price if book.sale_price > 0 else book.rental_price
        estimated_revenue += (book.wishlist_count * price)
    
    context = {
        'wishlisted_books': wishlisted_books,
        'low_stock_books': low_stock_books[:10],
        'total_wishlisted': wishlisted_books.count(),
        'popular_count': wishlisted_books.filter(wishlist_count__gte=5).count(),
        'low_stock_count': low_stock_books.count(),
        'trending_count': wishlisted_books.filter(created_at__gte=datetime.now() - timedelta(days=7)).count(),
        'estimated_revenue': estimated_revenue,
    }
    
    return render(request, 'store/wishlist.html', context)




















# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

def contact(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        newsletter = request.POST.get('newsletter', '')
        
        # Prepare email content
        email_subject = f"Contact Form: {subject}"
        email_message = f"""
Contact Form Submission from BookHub

Name: {first_name} {last_name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}

Newsletter Subscription: {'Yes' if newsletter == 'yes' else 'No'}
        """
        
        try:
            # Send email
            send_mail(
                email_subject,
                email_message,
                email,  # From email (sender's email)
                ['lastherio9396@gmail.com'],  # To email
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again.')
        
        return redirect('contact')
    
    return render(request, 'contact.html')

# --- Added missing views for privacy policy, terms of service, and FAQ ---
from django.views.decorators.http import require_GET

@require_GET
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

@require_GET
def terms_of_service(request):
    return render(request, 'terms_of_service.html')

@require_GET
def faq(request):
    return render(request, 'faq.html')













# Add these imports at the top of your views.py if not already present
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json














@login_required
def profile(request):
    """Main profile page for users to update their information"""
    account_type = get_account_type(request.user)
    stores = get_managed_stores(request.user) if account_type == STORE_OWNER_GROUP else None
    
    # Get user's orders
    orders = Order.objects.filter(customer=request.user)
    total_orders = orders.count()
    active_orders = orders.filter(status__in=['pending', 'approved', 'preparing', 'ready', 'out_for_delivery']).count()
    completed_orders = orders.filter(status='completed').count()
    
    # Get wishlist count
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    # Get user preferences (you can create a UserProfile model for these)
    preferences = {
        'email_notifications': True,
        'order_updates': True,
        'promotional_emails': False,
        'profile_public': True,
    }
    
    context = {
        'account_type': account_type,
        'stores': stores,
        'total_orders': total_orders,
        'active_orders': active_orders,
        'completed_orders': completed_orders,
        'wishlist_count': wishlist_count,
        'preferences': preferences,
    }
    return render(request, 'profile.html', context)

@login_required
@require_POST
def update_profile(request):
    """Update user's personal information"""
    try:
        user = request.user
        
        # Update username
        username = request.POST.get('username')
        if username and username != user.username:
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, 'Username already taken')
                return redirect('profile')
            user.username = username
        
        # Update name
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        
        # Update email
        email = request.POST.get('email')
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, 'Email already registered')
                return redirect('profile')
            user.email = email
        
        # Update phone (if you have a UserProfile model)
        # For now, we'll store it in session or you can create a UserProfile model
        if hasattr(user, 'profile'):
            user.profile.phone = request.POST.get('phone', '')
            user.profile.save()
        
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
    except Exception as e:
        messages.error(request, f'Error updating profile: {str(e)}')
    
    return redirect('profile')

@login_required
@require_POST
def update_account(request):
    """Update account settings and password"""
    try:
        user = request.user
        
        # Update account type (add/remove groups)
        new_account_type = request.POST.get('account_type')
        if new_account_type in VALID_ACCOUNT_TYPES:
            # Remove from all groups
            user.groups.clear()
            # Add to selected group
            group, _ = Group.objects.get_or_create(name=new_account_type)
            user.groups.add(group)
        
        # Change password if provided
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        
        if current_password and new_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Password changed successfully!')
            else:
                messages.error(request, 'Current password is incorrect')
                return redirect('profile')
        
        messages.success(request, 'Account settings updated successfully!')
    except Exception as e:
        messages.error(request, f'Error updating account: {str(e)}')
    
    return redirect('profile')

@login_required
@require_POST
def update_preferences(request):
    """Update user preferences"""
    try:
        # Here you would save preferences to a UserProfile model
        # For now, we'll just show a success message
        messages.success(request, 'Preferences updated successfully!')
    except Exception as e:
        messages.error(request, f'Error updating preferences: {str(e)}')
    
    return redirect('profile')

@login_required
@require_POST
def update_avatar(request):
    """Update user avatar via AJAX"""
    try:
        # Handle avatar upload
        # You'll need to add an ImageField to your User model or create a UserProfile model
        if request.FILES.get('avatar'):
            # Save the file
            # user.profile.avatar = request.FILES['avatar']
            # user.profile.save()
            return JsonResponse({'success': True, 'message': 'Avatar updated successfully'})
        return JsonResponse({'success': False, 'message': 'No file uploaded'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def delete_account(request):
    """Delete user account"""
    if request.method == 'POST':
        user = request.user
        # Logout first
        logout(request)
        # Delete user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('index')
    return render(request, 'delete_account_confirm.html')















    #store

    




















    















    


@login_required
def profile_store_owner(request):
    """Main profile page for users to update their information"""
    account_type = get_account_type(request.user)
    stores = get_managed_stores(request.user) if account_type == STORE_OWNER_GROUP else None
    
    # Get user's orders
    orders = Order.objects.filter(customer=request.user)
    total_orders = orders.count()
    active_orders = orders.filter(status__in=['pending', 'approved', 'preparing', 'ready', 'out_for_delivery']).count()
    completed_orders = orders.filter(status='completed').count()
    
    # Get wishlist count
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    # Get user preferences (you can create a UserProfile model for these)
    preferences = {
        'email_notifications': True,
        'order_updates': True,
        'promotional_emails': False,
        'profile_public': True,
    }
    
    context = {
        'account_type': account_type,
        'stores': stores,
        'total_orders': total_orders,
        'active_orders': active_orders,
        'completed_orders': completed_orders,
        'wishlist_count': wishlist_count,
        'preferences': preferences,
    }
    return render(request, 'profile_store_owner.html', context)

@login_required
@require_POST
def update_profile_store_owner(request):
    """Update user's personal information"""
    try:
        user = request.user
        
        # Update username
        username = request.POST.get('username')
        if username and username != user.username:
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, 'Username already taken')
                return redirect('profile_store_owner')
            user.username = username
        
        # Update name
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        
        # Update email
        email = request.POST.get('email')
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, 'Email already registered')
                return redirect('profile_store_owner')
            user.email = email
        
        # Update phone (if you have a UserProfile model)
        # For now, we'll store it in session or you can create a UserProfile model
        if hasattr(user, 'profile'):
            user.profile.phone = request.POST.get('phone', '')
            user.profile.save()
        
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
    except Exception as e:
        messages.error(request, f'Error updating profile: {str(e)}')
    
    return redirect('store/profile_store_owner.html') ,

@login_required
@require_POST
def update_account_store_owner(request):
    """Update account settings and password"""
    try:
        user = request.user
        
        # Update account type (add/remove groups)
        new_account_type = request.POST.get('account_type')
        if new_account_type in VALID_ACCOUNT_TYPES:
            # Remove from all groups
            user.groups.clear()
            # Add to selected group
            group, _ = Group.objects.get_or_create(name=new_account_type)
            user.groups.add(group)
        
        # Change password if provided
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        
        if current_password and new_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Password changed successfully!')
            else:
                messages.error(request, 'Current password is incorrect')
                return redirect('profile_store_owner')
        
        messages.success(request, 'Account settings updated successfully!')
    except Exception as e:
        messages.error(request, f'Error updating account: {str(e)}')
    
    return redirect('profile_store_owner')

@login_required
@require_POST
def update_preferences_store_owner(request):
    """Update user preferences"""
    try:
        # Here you would save preferences to a UserProfile model
        # For now, we'll just show a success message
        messages.success(request, 'Preferences updated successfully!')
    except Exception as e:
        messages.error(request, f'Error updating preferences: {str(e)}')
    
    return redirect('profile_store_owner')

@login_required
@require_POST
def update_avatar_store_owner(request):
    """Update user avatar via AJAX"""
    try:
        # Handle avatar upload
        # You'll need to add an ImageField to your User model or create a UserProfile model
        if request.FILES.get('avatar'):
            # Save the file
            # user.profile.avatar = request.FILES['avatar']
            # user.profile.save()
            return JsonResponse({'success': True, 'message': 'Avatar updated successfully'})
        return JsonResponse({'success': False, 'message': 'No file uploaded'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def delete_account_store_owner(request):
    """Delete user account"""
    if request.method == 'POST':
        user = request.user
        # Logout first
        logout(request)
        # Delete user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('store_dashboard')
    return render(request, 'delete_account_store.html')















    #store

    




















    