from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
import json
import os
import random
from decimal import Decimal
from django.contrib.auth.models import User, Group
from .models import (
    Features,
    Store,
    Book,
    Order,
    OrderItem,
    Delivery,
    CustomerReview,
    Wishlist,
    Conversation,
    Message,
    AdminAccount,
    AccountRestriction,
    IssueReport,
    SupportConversation,
    SupportMessage,
    ModerationActivityLog,
    UserProfile,
)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.forms import ModelForm
from datetime import datetime, timedelta
from django.db.models import Sum, Q, Count
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.utils import timezone
from functools import wraps


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


def get_managed_stores(user):
    if not user.is_authenticated:
        return Store.objects.none()

    if user.is_superuser or user.is_staff or user.username.lower() in ('admin', 'administrator'):
        return Store.objects.all()

    # Primary ownership mapping for store-owner accounts.
    store_filter = Q(owner=user)
    has_filter = True

    name_candidates = {user.username}
    full_name = user.get_full_name().strip()
    if full_name:
        name_candidates.add(full_name)

    for candidate in name_candidates:
        value = (candidate or '').strip()
        if not value:
            continue
        store_filter |= Q(owner_full_name__iexact=value)

    if user.email:
        store_filter |= Q(email__iexact=user.email.strip())

    return Store.objects.filter(store_filter).distinct() if has_filter else Store.objects.none()


def can_manage_order(user, order):
    if not user.is_authenticated or get_account_type(user) != STORE_OWNER_GROUP:
        return False
    if user.is_superuser:
        return True
    return get_managed_stores(user).filter(id=order.id).exists()


STORE_OWNER_GROUP = "store_owner"
CUSTOMER_GROUP = "customer"
VALID_ACCOUNT_TYPES = {STORE_OWNER_GROUP, CUSTOMER_GROUP}
IMAGE_ATTACHMENT_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"}
MAX_AVATAR_UPLOAD_SIZE = 5 * 1024 * 1024


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


def super_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Only the Super Admin can access this page.")
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)

    return wrapper


def clear_normal_admin_session(request):
    request.session.pop("normal_admin_id", None)
    request.session.pop("normal_admin_name", None)
    request.session.pop("normal_admin_type", None)


def get_current_normal_admin(request):
    admin_account_id = request.session.get("normal_admin_id")
    if not admin_account_id:
        return None
    admin_account = AdminAccount.objects.filter(id=admin_account_id).first()
    if not admin_account:
        clear_normal_admin_session(request)
        return None
    return admin_account


def normal_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            messages.error(request, "Super Admin cannot use Sub-Admin tools.")
            return redirect('dashboard_super')

        admin_account = get_current_normal_admin(request)
        if not admin_account:
            messages.error(request, "Please log in as Sub-Admin to access this page.")
            return redirect('normal_admin_login')

        if admin_account.status == AdminAccount.STATUS_DELETED:
            clear_normal_admin_session(request)
            messages.error(request, "This Sub-Admin account has been deleted.")
            return redirect('normal_admin_login')

        if admin_account.is_currently_suspended():
            clear_normal_admin_session(request)
            until_text = ""
            if admin_account.suspension_until:
                until_text = timezone.localtime(admin_account.suspension_until).strftime('%Y-%m-%d %H:%M')
                until_text = f" until {until_text}"
            reason_text = admin_account.suspension_reason or "No reason was provided."
            messages.error(request, f"Sub-Admin account is suspended{until_text}. Reason: {reason_text}")
            return redirect('normal_admin_login')

        request.normal_admin = admin_account
        return view_func(request, *args, **kwargs)

    return wrapper


def get_user_role_for_platform(user):
    if user.groups.filter(name=STORE_OWNER_GROUP).exists() or get_managed_stores(user).exists():
        return STORE_OWNER_GROUP
    return CUSTOMER_GROUP


def get_or_create_restriction(user):
    restriction, _ = AccountRestriction.objects.get_or_create(user=user)
    return restriction


def get_restriction_message(user):
    restriction = AccountRestriction.objects.filter(user=user).first()
    if not restriction:
        return ""
    return restriction.status_message()


def get_admin_actor_context(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return {
            "actor_role": ModerationActivityLog.ACTOR_ADMIN,
            "actor_name": request.user.get_username(),
            "admin_account": None,
        }

    admin_account = get_current_normal_admin(request)
    if admin_account:
        return {
            "actor_role": ModerationActivityLog.ACTOR_SUB_ADMIN,
            "actor_name": admin_account.name,
            "admin_account": admin_account,
        }

    return {
        "actor_role": ModerationActivityLog.ACTOR_SYSTEM,
        "actor_name": "System",
        "admin_account": None,
    }


def create_activity_log(action, actor_role, actor_name, target_type, target_identifier, reason="", metadata=None):
    ModerationActivityLog.objects.create(
        action=action,
        actor_role=actor_role,
        actor_name=actor_name,
        target_type=target_type,
        target_identifier=target_identifier,
        reason=reason or "",
        metadata=metadata or {},
    )


def notify_user_by_email(user, subject, body):
    if not user.email:
        return
    send_mail(
        subject=subject,
        message=body,
        from_email=None,
        recipient_list=[user.email],
        fail_silently=True,
    )


def get_default_active_sub_admin():
    return AdminAccount.objects.filter(status=AdminAccount.STATUS_ACTIVE).order_by('created_at').first()


def get_support_sender_name(message_obj):
    if message_obj.sender_sub_admin:
        return message_obj.sender_sub_admin.name
    if message_obj.sender_user:
        full_name = message_obj.sender_user.get_full_name().strip()
        return full_name or message_obj.sender_user.username
    return message_obj.sender_role.replace('_', ' ').title()


def get_or_create_user_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def get_user_avatar_url(user):
    profile = UserProfile.objects.filter(user=user).first()
    if profile and profile.avatar:
        return profile.avatar.url
    return ""


def get_admin_account_avatar_url(admin_account):
    if admin_account and admin_account.profile_image:
        return admin_account.profile_image.url
    return ""


def validate_avatar_file(avatar_file):
    if not avatar_file:
        return "No file uploaded."

    _, extension = os.path.splitext((avatar_file.name or "").lower())
    if extension not in IMAGE_ATTACHMENT_EXTENSIONS:
        return "Only image files are allowed (JPG, JPEG, PNG, GIF, WEBP, BMP, SVG)."

    if avatar_file.size > MAX_AVATAR_UPLOAD_SIZE:
        return "Image size must be 5MB or less."

    return ""


def save_user_avatar(user, avatar_file):
    profile = get_or_create_user_profile(user)
    if profile.avatar:
        profile.avatar.delete(save=False)
    profile.avatar = avatar_file
    profile.save(update_fields=['avatar', 'updated_at'])
    return profile.avatar.url


def save_admin_account_avatar(admin_account, avatar_file):
    if admin_account.profile_image:
        admin_account.profile_image.delete(save=False)
    admin_account.profile_image = avatar_file
    admin_account.save(update_fields=['profile_image'])
    return admin_account.profile_image.url


def is_image_attachment(file_field):
    if not file_field:
        return False
    filename = getattr(file_field, "name", "") or ""
    _, extension = os.path.splitext(filename.lower())
    return extension in IMAGE_ATTACHMENT_EXTENSIONS


def build_issue_report_subject(report):
    return f"Issue Report #{report.id}: {report.get_category_display()}"


def build_issue_report_auto_message(report):
    return (
        f"Issue Report #{report.id}\n"
        f"Category: {report.get_category_display()}\n"
        f"Reporter: {report.reporter.username} ({report.get_reporter_role_display()})\n"
        f"Reported User: {report.reported_user.username}\n\n"
        f"{report.description}"
    )


def build_sub_admin_escalation_message(report, sub_admin_name, note=""):
    if report:
        message = (
            f"Escalated by Sub-Admin: {sub_admin_name}\n"
            f"Issue Report #{report.id}\n"
            f"Category: {report.get_category_display()}\n"
            f"Reporter: {report.reporter.username} ({report.get_reporter_role_display()})\n"
            f"Reported User: {report.reported_user.username}\n"
            f"Current Status: {report.get_status_display()}"
        )
    else:
        message = f"Escalated by Sub-Admin: {sub_admin_name}\nSupport conversation requires Super Admin review."

    if note:
        message = f"{message}\n\nSub-Admin Note:\n{note}"
    return message


def get_or_create_issue_support_conversation(report, target):
    default_subject = build_issue_report_subject(report)
    if target == SupportConversation.TARGET_ADMIN:
        default_subject = f"Escalated: {default_subject}"

    conversation, _ = SupportConversation.objects.get_or_create(
        user=report.reporter,
        issue_report=report,
        target=target,
        defaults={
            "user_role": report.reporter_role,
            "subject": default_subject,
            "assigned_sub_admin": report.assigned_sub_admin,
        },
    )

    update_fields = []
    if conversation.user_role != report.reporter_role:
        conversation.user_role = report.reporter_role
        update_fields.append('user_role')
    if not conversation.subject:
        conversation.subject = default_subject
        update_fields.append('subject')
    if report.assigned_sub_admin_id and conversation.assigned_sub_admin_id != report.assigned_sub_admin_id:
        conversation.assigned_sub_admin_id = report.assigned_sub_admin_id
        update_fields.append('assigned_sub_admin')
    if update_fields:
        conversation.save(update_fields=update_fields + ['updated_at'])

    return conversation


def seed_issue_report_support_thread(report):
    conversation = get_or_create_issue_support_conversation(report, SupportConversation.TARGET_SUB_ADMIN)
    SupportMessage.objects.create(
        conversation=conversation,
        sender_user=report.reporter,
        sender_role=report.reporter_role,
        content=build_issue_report_auto_message(report),
        attachment=report.attachment if report.attachment else None,
        is_read=False,
    )
    return conversation


def build_admin_ref_number():
    """Generate a unique reference number in ADM-YYYY-NNNN format."""
    year = timezone.now().year

    for _ in range(100):
        candidate = f"ADM-{year}-{random.randint(1, 9999):04d}"
        if not AdminAccount.objects.filter(ref_number=candidate).exists():
            return candidate

    # Fallback to deterministic scan if random attempts collide.
    next_seq = 1
    while True:
        candidate = f"ADM-{year}-{next_seq:04d}"
        if not AdminAccount.objects.filter(ref_number=candidate).exists():
            return candidate
        next_seq += 1


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
        login_mode = (request.POST.get("login_mode") or "").strip()

        # Normal Admin login (name + reference number).
        if login_mode == "normal_admin":
            admin_name = (request.POST.get("admin_name") or "").strip()
            ref_number = (request.POST.get("ref_number") or "").strip()

            if not admin_name or not ref_number:
                messages.error(request, "Admin name and reference number are required.")
                return redirect('normal_admin_login')

            admin_account = AdminAccount.objects.filter(
                name__iexact=admin_name,
                ref_number__iexact=ref_number,
            ).first()

            if not admin_account:
                messages.error(request, "Invalid admin name or reference number.")
                return redirect('normal_admin_login')

            if admin_account.status == AdminAccount.STATUS_DELETED:
                messages.error(request, "This Sub-Admin account has been deleted.")
                return redirect('normal_admin_login')

            if admin_account.is_currently_suspended():
                until_text = ""
                if admin_account.suspension_until:
                    until_text = timezone.localtime(admin_account.suspension_until).strftime('%Y-%m-%d %H:%M')
                    until_text = f" until {until_text}"
                reason_text = admin_account.suspension_reason or "No reason was provided."
                messages.error(request, f"Sub-Admin account is suspended{until_text}. Reason: {reason_text}")
                return redirect('normal_admin_login')

            # Keep this flow independent from Django user auth.
            if request.user.is_authenticated:
                auth_logout(request)
            clear_normal_admin_session(request)
            request.session["normal_admin_id"] = admin_account.id
            request.session["normal_admin_name"] = admin_account.name
            request.session["normal_admin_type"] = admin_account.admin_type
            messages.success(request, f"Welcome, {admin_account.name}!")
            return redirect('dashboard_admin')

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            restriction_message = get_restriction_message(user)
            if restriction_message:
                messages.error(request, restriction_message)
                return redirect('login')

            login(request, user)
            if get_account_type(user) == STORE_OWNER_GROUP:
                return redirect('store_dashboard')
            return redirect('customer_dashboard')

        candidate_user = User.objects.filter(username=username).first()
        if candidate_user:
            restriction_message = get_restriction_message(candidate_user)
            if restriction_message:
                messages.error(request, restriction_message)
                return redirect('login')

        messages.error(request, "Invalid credentials")
        return redirect('login')
    return render(request, "login.html")


def logout(request):
    clear_normal_admin_session(request)
    if request.user.is_authenticated:
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
        delivery_methods = request.POST.getlist("delivery_methods")
        delivery_bike = "bike" in delivery_methods or request.POST.get("delivery_bike")
        delivery_car = "car" in delivery_methods or request.POST.get("delivery_car")
        delivery_pickup = "pickup" in delivery_methods or request.POST.get("delivery_pickup")

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
        payment_methods_list = request.POST.getlist("payment_methods")
        if payment_methods_list:
            payment_methods = ", ".join(payment_methods_list)
        else:
            payment_methods = none_if_empty(request.POST.get("payment_methods"))
        agree_terms = to_bool(request.POST.get("agree_terms"))

        owner_user = request.user if request.user.is_authenticated else None
        if owner_user and not owner_full_name:
            owner_full_name = owner_user.get_full_name().strip() or owner_user.username

        if store_name and owner_full_name:
            if Store.objects.filter(store_name=store_name).exists():
                messages.info(request, "store name already exists")
                return redirect('store_registration')
            else:
                store = Store.objects.create(
                    store_name=store_name,
                    owner_full_name=owner_full_name,
                    owner=owner_user,
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
                messages.success(request, "Store registration successful.")
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
    stores = get_managed_stores(request.user)
    
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
    
    # compute account owner name (similar to context processor)
    primary_store = stores.first()
    account_owner = (
        primary_store.owner_full_name
        if primary_store and getattr(primary_store, 'owner_full_name', None)
        else (request.user.get_full_name().strip() or request.user.username)
    )

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
        'account_owner': account_owner,
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
        
        # Handle image upload
        cover_image = request.FILES.get('cover_image')

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
                # Update image if new one provided
                if cover_image:
                    # Delete old image if it exists
                    if existing_book.cover_image:
                        existing_book.cover_image.delete(save=False)
                    existing_book.cover_image = cover_image
                existing_book.save()
                messages.info(request, f"Book updated successfully in {store.store_name}.")
            else:
                # Create new book with store and image
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
                    store=store,
                    cover_image=cover_image,  # Save the uploaded image
                )
                messages.success(request, f"Book added successfully to {store.store_name}!")
             
            return redirect('add_book_registration')

        messages.info(request, "Title and Author are required")
        return redirect('add_book')

    return render(request, "store/add_book.html")


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
        
        # Handle image upload
        cover_image = request.FILES.get('cover_image')
        
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
        
        # Update image if new one provided
        if cover_image:
            # Delete old image if it exists
            if book.cover_image:
                book.cover_image.delete(save=False)
            book.cover_image = cover_image
        
        book.save()
        messages.success(request, "Book updated successfully.")
        return redirect('view_inventory')
    
    return render(request, 'store/edit_book.html', {'book': book})


#store registration view and edit and delete
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
    
    # Delete the cover image file when deleting the book
    if book.cover_image:
        book.cover_image.delete(save=False)
        
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('view_inventory')

    book.delete()
    messages.success(request, "Book deleted successfully.")
    return redirect('view_inventory')


# Update the customer_dashboard view with pagination and image display
def customer_dashboard(request):
    # Get all books with stores
    books = Book.objects.select_related('store').filter(store__isnull=False)
    
    # Debug: Print first few books
    print("\n=== DEBUG: First 5 Books ===")
    for book in books[:5]:
        print(f"Book: {book.title}")
        print(f"  Available Copies (rent): {book.available_copies}")
        print(f"  Available Sales (purchase): {book.available_sales}")
        print(f"  Total Copies: {book.total_copies}")
        print(f"  Has Cover Image: {bool(book.cover_image)}")
    print("=== END DEBUG ===\n")

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
# NOTE: old implementation removed in favor of _build_store_orders_context below
# @login_required
# def store_orders(request):
#     # legacy code no longer used
#     pass


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
    # Clear session wishlist
    if 'wishlist' in request.session:
        request.session['wishlist'] = []
        request.session.modified = True

    # Also clear DB wishlist for authenticated users
    if request.user.is_authenticated:
        Wishlist.objects.filter(user=request.user).delete()

    messages.success(request, "Wishlist cleared.")
    return redirect('wishlist')


def wishlist(request):
    # Show wishlist for current user or session
    if request.user.is_authenticated:
        # Migrate legacy session wishlist items into DB-backed wishlist.
        session_ids = request.session.get('wishlist', [])
        if session_ids:
            books_from_session = list(Book.objects.filter(id__in=session_ids).only('id'))
            if books_from_session:
                Wishlist.objects.bulk_create(
                    [Wishlist(user=request.user, book=book) for book in books_from_session],
                    ignore_conflicts=True,
                )
            request.session['wishlist'] = []
            request.session.modified = True

        wishlist_items = (
            Wishlist.objects
            .filter(user=request.user)
            .select_related('book', 'book__store', 'book__store__owner', 'book__store__owner__user_profile')
            .order_by('-created_at')
        )
        wishlist_books = [item.book for item in wishlist_items if item.book_id]
    else:
        ids = request.session.get('wishlist', [])
        wishlist_books = list(
            Book.objects.filter(id__in=ids).select_related('store', 'store__owner', 'store__owner__user_profile')
        )

    for book in wishlist_books:
        store = getattr(book, 'store', None)
        owner_name = "Store Owner"
        owner_avatar_url = ""

        if store:
            fallback_name = (getattr(store, 'owner_full_name', '') or '').strip()
            if fallback_name:
                owner_name = fallback_name

            owner = getattr(store, 'owner', None)
            if owner:
                full_name = owner.get_full_name().strip()
                if full_name:
                    owner_name = full_name
                elif owner.username:
                    owner_name = owner.username

                try:
                    owner_profile = owner.user_profile
                except UserProfile.DoesNotExist:
                    owner_profile = None
                if owner_profile and owner_profile.avatar:
                    owner_avatar_url = owner_profile.avatar.url

        book.store_owner_name = owner_name
        book.store_owner_avatar_url = owner_avatar_url

    context = {
        # Keep both keys for backward compatibility across templates.
        'wishlist_books': wishlist_books,
        'wishlist_count': len(wishlist_books),
        'books': wishlist_books,
    }
    return render(request, 'customer/wishlist.html', context)


@login_required
def add_to_wishlist(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('customer_dashboard')

    # Create wishlist entry if not exists
    Wishlist.objects.get_or_create(user=request.user, book=book)
    messages.success(request, f"Added '{book.title}' to your wishlist.")
    return redirect('book_detail', book_id=book_id)


@login_required
def remove_from_wishlist(request, book_id):
    if request.user.is_authenticated:
        Wishlist.objects.filter(user=request.user, book_id=book_id).delete()
        messages.success(request, "Removed item from wishlist.")
    else:
        # Fallback for session-based wishlist
        ids = request.session.get('wishlist', [])
        if book_id in ids:
            ids.remove(book_id)
            request.session['wishlist'] = ids
            request.session.modified = True
            messages.success(request, "Removed item from wishlist.")

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


def _build_store_orders_context(request):
    # Get stores owned by the user
    stores = get_managed_stores(request.user)
    if not stores.exists():
        messages.info(request, "No store assigned to this account yet. Showing empty order management.")

    # compute account_owner for header display (primary store owner name or fallback to user)
    primary_store = stores.first()
    account_owner = (
        primary_store.owner_full_name
        if primary_store and getattr(primary_store, 'owner_full_name', None)
        else (request.user.get_full_name().strip() or request.user.username)
    )

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
        'account_owner': account_owner,
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


# Contact and static pages
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


# Profile management
@login_required
def profile(request):
    """Main profile page for users to update their information"""
    account_type = get_account_type(request.user)
    stores = get_managed_stores(request.user) if account_type == STORE_OWNER_GROUP else None
    avatar_url = get_user_avatar_url(request.user)
    
    # Get user's orders
    orders = Order.objects.filter(customer=request.user)
    total_orders = orders.count()
    active_orders = orders.filter(status__in=['pending', 'approved', 'preparing', 'ready', 'out_for_delivery']).count()
    completed_orders = orders.filter(status='completed').count()
    
    # Get wishlist count
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    # Get user preferences
    preferences = {
        'email_notifications': True,
        'order_updates': True,
        'promotional_emails': False,
        'profile_public': True,
    }
    
    context = {
        'account_type': account_type,
        'avatar_url': avatar_url,
        'stores': stores,
        'total_orders': total_orders,
        'active_orders': active_orders,
        'completed_orders': completed_orders,
        'wishlist_count': wishlist_count,
        'preferences': preferences,
    }
    return render(request, 'profile.html', context)


@login_required
def customer_profile(request):
    # Reuse the main `profile` view for customer-facing profile page
    return profile(request)


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
        messages.success(request, 'Preferences updated successfully!')
    except Exception as e:
        messages.error(request, f'Error updating preferences: {str(e)}')
    
    return redirect('profile')


@login_required
@require_POST
def update_avatar(request):
    """Update user avatar via AJAX"""
    try:
        avatar = request.FILES.get('avatar')
        validation_error = validate_avatar_file(avatar)
        if validation_error:
            return JsonResponse({'success': False, 'message': validation_error}, status=400)

        avatar_url = save_user_avatar(request.user, avatar)
        return JsonResponse(
            {
                'success': True,
                'message': 'Avatar updated successfully',
                'avatar_url': avatar_url,
            }
        )
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


# Store Owner Profile
@login_required
def profile_store_owner(request):
    """Main profile page for store owners"""
    account_type = get_account_type(request.user)
    stores = get_managed_stores(request.user) if account_type == STORE_OWNER_GROUP else None
    avatar_url = get_user_avatar_url(request.user)
    
    # Get user's orders
    orders = Order.objects.filter(customer=request.user)
    total_orders = orders.count()
    active_orders = orders.filter(status__in=['pending', 'approved', 'preparing', 'ready', 'out_for_delivery']).count()
    completed_orders = orders.filter(status='completed').count()
    
    # Get wishlist count
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    # Get user preferences
    preferences = {
        'email_notifications': True,
        'order_updates': True,
        'promotional_emails': False,
        'profile_public': True,
    }
    
    context = {
        'account_type': account_type,
        'avatar_url': avatar_url,
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
        
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
    except Exception as e:
        messages.error(request, f'Error updating profile: {str(e)}')
    
    return redirect('profile_store_owner')


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
        messages.success(request, 'Preferences updated successfully!')
    except Exception as e:
        messages.error(request, f'Error updating preferences: {str(e)}')
    
    return redirect('profile_store_owner')


@login_required
@require_POST
def update_avatar_store_owner(request):
    """Update user avatar via AJAX"""
    try:
        avatar = request.FILES.get('avatar')
        validation_error = validate_avatar_file(avatar)
        if validation_error:
            return JsonResponse({'success': False, 'message': validation_error}, status=400)

        avatar_url = save_user_avatar(request.user, avatar)
        return JsonResponse(
            {
                'success': True,
                'message': 'Avatar updated successfully',
                'avatar_url': avatar_url,
            }
        )
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@super_admin_required
def super_admin_profile(request):
    context = {
        'avatar_url': get_user_avatar_url(request.user),
    }
    return render(request, 'admin/super_admin_profile.html', context)


@super_admin_required
@require_POST
def super_admin_profile_update(request):
    user = request.user
    username = (request.POST.get('username') or '').strip()
    first_name = (request.POST.get('first_name') or '').strip()
    last_name = (request.POST.get('last_name') or '').strip()
    email = (request.POST.get('email') or '').strip()

    if username and username != user.username:
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, 'Username already taken.')
            return redirect('super_admin_profile')
        user.username = username

    if email and email != user.email:
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'Email already registered.')
            return redirect('super_admin_profile')
        user.email = email

    user.first_name = first_name
    user.last_name = last_name
    user.save()
    messages.success(request, 'Super Admin profile updated successfully.')
    return redirect('super_admin_profile')


@super_admin_required
@require_POST
def super_admin_update_avatar(request):
    try:
        avatar = request.FILES.get('avatar')
        validation_error = validate_avatar_file(avatar)
        if validation_error:
            return JsonResponse({'success': False, 'message': validation_error}, status=400)

        avatar_url = save_user_avatar(request.user, avatar)
        return JsonResponse(
            {
                'success': True,
                'message': 'Avatar updated successfully',
                'avatar_url': avatar_url,
            }
        )
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@normal_admin_required
def sub_admin_profile(request):
    admin_account = request.normal_admin
    context = {
        'admin_account': admin_account,
        'avatar_url': get_admin_account_avatar_url(admin_account),
        'is_normal_admin': True,
    }
    return render(request, 'admin/sub_admin_profile.html', context)


@normal_admin_required
@require_POST
def sub_admin_profile_update(request):
    admin_account = request.normal_admin
    name = (request.POST.get('name') or '').strip()
    email = (request.POST.get('email') or '').strip()
    admin_type = (request.POST.get('admin_type') or '').strip()

    if not name:
        messages.error(request, 'Name is required.')
        return redirect('sub_admin_profile')

    if email and AdminAccount.objects.filter(email__iexact=email).exclude(id=admin_account.id).exists():
        messages.error(request, 'Email is already in use by another admin account.')
        return redirect('sub_admin_profile')

    fields_to_update = []
    if admin_account.name != name:
        admin_account.name = name
        fields_to_update.append('name')
    if admin_account.email != email:
        admin_account.email = email
        fields_to_update.append('email')
    if admin_type and admin_account.admin_type != admin_type:
        admin_account.admin_type = admin_type
        fields_to_update.append('admin_type')

    if fields_to_update:
        admin_account.save(update_fields=fields_to_update)
        request.session["normal_admin_name"] = admin_account.name

    messages.success(request, 'Sub-Admin profile updated successfully.')
    return redirect('sub_admin_profile')


@normal_admin_required
@require_POST
def sub_admin_update_avatar(request):
    try:
        avatar = request.FILES.get('avatar')
        validation_error = validate_avatar_file(avatar)
        if validation_error:
            return JsonResponse({'success': False, 'message': validation_error}, status=400)

        avatar_url = save_admin_account_avatar(request.normal_admin, avatar)
        return JsonResponse(
            {
                'success': True,
                'message': 'Avatar updated successfully',
                'avatar_url': avatar_url,
            }
        )
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

















# Chat Views
@login_required
def start_or_get_conversation(request, store_id, book_id=None):
    """Start a new conversation or get existing one"""
    store = get_object_or_404(Store, id=store_id)
    book = None
    if book_id:
        book = get_object_or_404(Book, id=book_id, store=store)
    
    # Try to get existing conversation
    conversation = Conversation.objects.filter(
        customer=request.user,
        store=store,
        book=book
    ).first()
    
    # Create new if doesn't exist
    if not conversation:
        conversation = Conversation.objects.create(
            customer=request.user,
            store=store,
            book=book
        )
    
    return redirect('chat_room', conversation_id=conversation.id)


@login_required
def chat_room(request, conversation_id):
    """Display chat room for a conversation"""
    conversation = get_object_or_404(
        Conversation.objects.select_related('customer', 'store', 'book'),
        id=conversation_id
    )
    
    # Check if user is part of this conversation
    is_customer = conversation.customer == request.user
    is_store_owner = can_manage_order(request.user, conversation.store)
    
    if not (is_customer or is_store_owner):
        messages.error(request, "You don't have permission to view this chat.")
        if get_account_type(request.user) == STORE_OWNER_GROUP:
            return redirect('store_chat_list')
        return redirect('customer_dashboard')
    
    # Mark messages as read
    if is_customer:
        conversation.messages.exclude(sender=request.user).update(is_read=True)
    elif is_store_owner:
        conversation.messages.exclude(sender=request.user).update(is_read=True)
    
    # Get messages
    messages_list = conversation.messages.all()
    
    # Get other conversations for sidebar (for store owners)
    other_conversations = []
    if is_store_owner:
        other_conversations = Conversation.objects.filter(
            store=conversation.store
        ).exclude(id=conversation_id).select_related('customer', 'book')[:10]
    
    # Get unread counts
    unread_counts = {}
    if is_store_owner:
        for conv in other_conversations:
            unread_counts[conv.id] = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
    
    context = {
        'conversation': conversation,
        'messages': messages_list,
        'other_conversations': other_conversations,
        'unread_counts': unread_counts,
        'is_customer': is_customer,
        'is_store_owner': is_store_owner,
        'store': conversation.store,
        'book': conversation.book,
    }
    
    template_name = 'customer/chat_room.html' if is_customer else 'store/chat_detail.html'
    return render(request, template_name, context)


@login_required
@require_POST
def send_message(request, conversation_id):
    """Send a message (AJAX)"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check permission
    is_customer = conversation.customer == request.user
    is_store_owner = can_manage_order(request.user, conversation.store)
    
    if not (is_customer or is_store_owner):
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty'})
        
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        # Update conversation timestamp
        conversation.save()  # This will update auto_now field
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'formatted_time': message.formatted_time(),
                'sender': message.sender.username,
                'is_me': True
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def mark_messages_read(request, conversation_id):
    """Mark all messages in conversation as read"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check permission
    is_customer = conversation.customer == request.user
    is_store_owner = can_manage_order(request.user, conversation.store)
    
    if not (is_customer or is_store_owner):
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    conversation.messages.exclude(sender=request.user).update(is_read=True)
    
    return JsonResponse({'success': True})


@login_required
def get_unread_count(request):
    """Get total unread messages count for current user"""
    if get_account_type(request.user) == STORE_OWNER_GROUP:
        # Store owner: count unread messages from all conversations
        stores = get_managed_stores(request.user)
        conversations = Conversation.objects.filter(store__in=stores)
        unread_count = Message.objects.filter(
            conversation__in=conversations,
            is_read=False
        ).exclude(sender=request.user).count()
    else:
        # Customer: count unread messages from all conversations
        conversations = Conversation.objects.filter(customer=request.user)
        unread_count = Message.objects.filter(
            conversation__in=conversations,
            is_read=False
        ).exclude(sender=request.user).count()
    
    return JsonResponse({'unread_count': unread_count})


@login_required
def delete_conversation(request, conversation_id):
    """Delete a conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check permission
    is_customer = conversation.customer == request.user
    is_store_owner = can_manage_order(request.user, conversation.store)
    
    if not (is_customer or is_store_owner):
        messages.error(request, "You don't have permission to delete this conversation.")
        return redirect('customer_dashboard')
    
    if request.method == 'POST':
        conversation.delete()
        messages.success(request, "Conversation deleted successfully.")
        
        if is_store_owner:
            return redirect('store_chat_list')
        return redirect('customer_dashboard')
    
    return render(request, 'chat/delete_confirm.html', {'conversation': conversation})


# Store Owner Chat Management
@login_required
def store_chat_list(request):
    """Display list of all conversations for a store owner"""
    guard = ensure_store_owner(request)
    if guard:
        return guard
    
    stores = get_managed_stores(request.user)
    if not stores.exists():
        messages.info(request, "You don't have any stores yet.")
        return redirect('store_dashboard')
    
    # Get all conversations for these stores
    conversations = Conversation.objects.filter(
        store__in=stores
    ).select_related('customer', 'book', 'store').order_by('-updated_at')
    
    # Search by customer name or book title
    search_query = request.GET.get('search', '')
    if search_query:
        conversations = conversations.filter(
            Q(customer__username__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(book__title__icontains=search_query)
        )
    
    # Filter by store
    store_filter = request.GET.get('store', '')
    if store_filter:
        conversations = conversations.filter(store_id=store_filter)
    
    # Get unread counts for each conversation
    conversation_data = []
    for conv in conversations:
        last_msg = conv.last_message()
        unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
        conversation_data.append({
            'conversation': conv,
            'last_message': last_msg,
            'unread_count': unread_count,
        })
    
    # Get unread count for sidebar badge
    total_unread = Message.objects.filter(
        conversation__in=conversations,
        is_read=False
    ).exclude(sender=request.user).count()
    
    context = {
        'conversation_data': conversation_data,
        'stores': stores,
        'search_query': search_query,
        'selected_store': store_filter,
        'total_unread': total_unread,
    }
    
    return render(request, 'store/chats.html', context)


@login_required
def store_chat_detail(request, conversation_id):
    """Display a single conversation for a store owner"""
    guard = ensure_store_owner(request)
    if guard:
        return guard

    conversation = get_object_or_404(
        Conversation.objects.select_related('customer', 'store', 'book'),
        id=conversation_id
    )

    # Ensure this conversation belongs to one of the owner's managed stores
    stores = get_managed_stores(request.user)
    if conversation.store not in stores:
        messages.error(request, "You don't have permission to view this chat.")
        return redirect('store_chat_list')

    # Mark messages as read
    conversation.messages.exclude(sender=request.user).update(is_read=True)

    # Get messages
    messages_list = conversation.messages.all()

    # Get other conversations for sidebar
    other_conversations = Conversation.objects.filter(
        store=conversation.store
    ).exclude(id=conversation_id).select_related('customer', 'book')[:10]

    # Get unread counts for sidebar
    unread_counts = {conv.id: conv.messages.filter(is_read=False).exclude(sender=request.user).count() for conv in other_conversations}

    context = {
        'conversation': conversation,
        'messages': messages_list,
        'other_conversations': other_conversations,
        'unread_counts': unread_counts,
        'is_store_owner': True,
        'store': conversation.store,
        'book': conversation.book,
    }

    return render(request, 'store/chat_detail.html', context)



















@login_required
def customer_chat_list(request):
    """Display all conversations for a customer (WhatsApp style)"""
    # Get all conversations for this customer
    conversations = Conversation.objects.filter(
        customer=request.user
    ).select_related('store', 'book').order_by('-updated_at')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        conversations = conversations.filter(
            Q(store__store_name__icontains=search_query) |
            Q(book__title__icontains=search_query) |
            Q(messages__content__icontains=search_query)
        ).distinct()
    
    # Get unread counts and last messages
    conversation_data = []
    for conv in conversations:
        last_msg = conv.last_message()
        unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
        conversation_data.append({
            'conversation': conv,
            'last_message': last_msg,
            'unread_count': unread_count,
        })
    
    # Get total unread count for badge
    total_unread = Message.objects.filter(
        conversation__in=conversations,
        is_read=False
    ).exclude(sender=request.user).count()
    
    context = {
        'conversation_data': conversation_data,
        'search_query': search_query,
        'total_unread': total_unread,
    }
    
    return render(request, 'customer/chat_list.html', context)
@super_admin_required
def register_admin(request):
    """Create a normal admin account and generate a unique reference number."""
    context = {}

    if request.method == "POST":
        admin_name = (request.POST.get("admin_name") or "").strip()
        admin_type = (request.POST.get("admin_type") or "").strip()
        email = (request.POST.get("email") or "").strip()

        if not admin_name or not admin_type:
            messages.error(request, "Admin Name and Admin Type are required.")
            return render(request, "admin/register_admin.html", context)

        ref_number = build_admin_ref_number()
        admin_account = AdminAccount.objects.create(
            name=admin_name,
            admin_type=admin_type,
            email=email or None,
            ref_number=ref_number,
            created_by=request.user,
        )

        context.update({
            "generated_ref_number": admin_account.ref_number,
            "created_admin": admin_account,
        })
        messages.success(
            request,
            f"Admin account created for {admin_account.name}. Reference number generated.",
        )

    return render(request, "admin/register_admin.html", context)


@super_admin_required
def view_admins(request):
    search_query = (request.GET.get("search") or "").strip()
    admins = AdminAccount.objects.all()

    if search_query:
        admins = admins.filter(
            Q(name__icontains=search_query)
            | Q(admin_type__icontains=search_query)
            | Q(ref_number__icontains=search_query)
            | Q(email__icontains=search_query)
        )

    context = {
        "admins": admins,
        "search_query": search_query,
    }
    return render(request, "admin/view_admins.html", context)


@super_admin_required
def super_admin(request):
    """Super admin dashboard with overview of entire platform"""
    # Get counts
    total_users = User.objects.count()
    total_stores = Store.objects.count()
    total_books = Book.objects.count()
    total_orders = Order.objects.count()
    
    # Get pending orders
    pending_orders = Order.objects.filter(status='pending').count()
    
    # Get recent users
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Get recent stores
    recent_stores = Store.objects.order_by('-id')[:10]
    
    # Get recent orders
    recent_orders = Order.objects.select_related('customer', 'store').order_by('-created_at')[:10]
    
    # Get revenue stats
    today = timezone.now().date()
    
    # Today's revenue
    today_revenue = Order.objects.filter(
        created_at__date=today,
        status__in=['delivered', 'completed']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Weekly revenue
    week_ago = today - timedelta(days=7)
    weekly_revenue = Order.objects.filter(
        created_at__date__gte=week_ago,
        status__in=['delivered', 'completed']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Monthly revenue
    monthly_revenue = Order.objects.filter(
        created_at__month=today.month,
        created_at__year=today.year,
        status__in=['delivered', 'completed']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # User distribution
    customers_count = User.objects.filter(groups__name='customer').count()
    store_owners_count = User.objects.filter(groups__name='store_owner').count()
    admins_count = User.objects.filter(is_staff=True).count()
    
    # Order status distribution
    order_status_counts = {
        'pending': Order.objects.filter(status='pending').count(),
        'approved': Order.objects.filter(status='approved').count(),
        'preparing': Order.objects.filter(status='preparing').count(),
        'out_for_delivery': Order.objects.filter(status='out_for_delivery').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'completed': Order.objects.filter(status='completed').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }
    
    # Top stores by orders
    top_stores = Store.objects.annotate(
        order_count=Count('order')
    ).order_by('-order_count')[:5]
    
    # Top books by orders
    top_books = Book.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:5]

    total_issue_reports = IssueReport.objects.count()
    pending_issue_reports = IssueReport.objects.filter(status=IssueReport.STATUS_PENDING).count()
    open_admin_support_conversations = SupportConversation.objects.filter(
        target=SupportConversation.TARGET_ADMIN,
        status=SupportConversation.STATUS_OPEN,
    ).count()
    suspended_sub_admins = AdminAccount.objects.filter(status=AdminAccount.STATUS_SUSPENDED).count()
    
    latest_admin_accounts = AdminAccount.objects.all()[:8]

    context = {
        'total_users': total_users,
        'total_stores': total_stores,
        'total_books': total_books,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_admin_accounts': AdminAccount.objects.count(),
        'latest_admin_accounts': latest_admin_accounts,
        'recent_users': recent_users,
        'recent_stores': recent_stores,
        'recent_orders': recent_orders,
        'today_revenue': today_revenue,
        'weekly_revenue': weekly_revenue,
        'monthly_revenue': monthly_revenue,
        'customers_count': customers_count,
        'store_owners_count': store_owners_count,
        'admins_count': admins_count,
        'order_status_counts': order_status_counts,
        'top_stores': top_stores,
        'top_books': top_books,
        'total_issue_reports': total_issue_reports,
        'pending_issue_reports': pending_issue_reports,
        'open_admin_support_conversations': open_admin_support_conversations,
        'suspended_sub_admins': suspended_sub_admins,
    }
    
    return render(request, 'admin/dashboard_super.html', context)


@staff_member_required
def admin_users(request):
    """Manage all users"""
    users = User.objects.all().order_by('-date_joined')
    
    # Filter by user type
    user_type = request.GET.get('type', 'all')
    if user_type == 'customer':
        users = users.filter(groups__name='customer')
    elif user_type == 'store_owner':
        users = users.filter(groups__name='store_owner')
    elif user_type == 'admin':
        users = users.filter(is_staff=True)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    paginator = Paginator(users, 20)
    page = request.GET.get('page', 1)
    users_page = paginator.get_page(page)
    
    context = {
        'users': users_page,
        'user_type': user_type,
        'search_query': search_query,
    }
    return render(request, 'admin/users.html', context)


@staff_member_required
def admin_stores(request):
    """Manage all stores"""
    stores = Store.objects.all().order_by('-id')
    
    # Filter by city
    city_filter = request.GET.get('city', '')
    if city_filter:
        stores = stores.filter(city__icontains=city_filter)
    
    # Filter by service
    service_filter = request.GET.get('service', '')
    if service_filter == 'rent':
        stores = stores.filter(offers_rental=True)
    elif service_filter == 'sale':
        stores = stores.filter(offers_sale=True)
    elif service_filter == 'delivery':
        stores = stores.filter(offers_delivery=True)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        stores = stores.filter(
            Q(store_name__icontains=search_query) |
            Q(owner_full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    paginator = Paginator(stores, 20)
    page = request.GET.get('page', 1)
    stores_page = paginator.get_page(page)
    
    # Get cities for filter
    cities = Store.objects.values_list('city', flat=True).distinct()
    
    context = {
        'stores': stores_page,
        'cities': cities,
        'city_filter': city_filter,
        'service_filter': service_filter,
        'search_query': search_query,
    }
    return render(request, 'admin/stores.html', context)


@staff_member_required
def admin_books(request):
    """Manage all books"""
    books = Book.objects.select_related('store').all().order_by('-created_at')
    
    # Filter by store
    store_filter = request.GET.get('store', '')
    if store_filter:
        books = books.filter(store_id=store_filter)
    
    # Filter by genre
    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        books = books.filter(genre=genre_filter)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )
    
    paginator = Paginator(books, 20)
    page = request.GET.get('page', 1)
    books_page = paginator.get_page(page)
    
    # Get stores and genres for filters
    stores = Store.objects.all()
    genres = Book.objects.values_list('genre', flat=True).distinct()
    
    context = {
        'books': books_page,
        'stores': stores,
        'genres': genres,
        'store_filter': store_filter,
        'genre_filter': genre_filter,
        'search_query': search_query,
    }
    return render(request, 'admin/books.html', context)


@staff_member_required
def admin_orders(request):
    """Manage all orders"""
    orders = Order.objects.select_related('customer', 'store').all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)
    
    # Filter by store
    store_filter = request.GET.get('store', '')
    if store_filter:
        orders = orders.filter(store_id=store_filter)
    
    # Filter by date
    date_filter = request.GET.get('date', 'all')
    today = timezone.now().date()
    if date_filter == 'today':
        orders = orders.filter(created_at__date=today)
    elif date_filter == 'week':
        week_ago = today - timedelta(days=7)
        orders = orders.filter(created_at__date__gte=week_ago)
    elif date_filter == 'month':
        month_ago = today - timedelta(days=30)
        orders = orders.filter(created_at__date__gte=month_ago)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(customer__username__icontains=search_query) |
            Q(customer__email__icontains=search_query)
        )
    
    paginator = Paginator(orders, 20)
    page = request.GET.get('page', 1)
    orders_page = paginator.get_page(page)
    
    # Get stores for filter
    stores = Store.objects.all()
    
    context = {
        'orders': orders_page,
        'stores': stores,
        'status_filter': status_filter,
        'store_filter': store_filter,
        'date_filter': date_filter,
        'search_query': search_query,
    }
    return render(request, 'admin/orders.html', context)


@staff_member_required
def admin_order_detail(request, order_id):
    """View order details as admin"""
    order = get_object_or_404(Order.objects.select_related('customer', 'store'), id=order_id)
    items = order.items.select_related('book').all()
    
    try:
        delivery = Delivery.objects.get(order=order)
    except Delivery.DoesNotExist:
        delivery = None
    
    context = {
        'order': order,
        'items': items,
        'delivery': delivery,
    }
    return render(request, 'admin/order_detail.html', context)


@staff_member_required
def admin_reports(request):
    """Generate platform reports"""
    today = timezone.now().date()
    
    # Date range for reports
    start_date = request.GET.get('start_date', (today - timedelta(days=30)).isoformat())
    end_date = request.GET.get('end_date', today.isoformat())
    
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except:
        start = today - timedelta(days=30)
        end = today
    
    # Orders in date range
    orders = Order.objects.filter(
        created_at__date__gte=start,
        created_at__date__lte=end
    )
    
    # Revenue report
    total_revenue = orders.filter(
        status__in=['delivered', 'completed']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Orders by store
    orders_by_store = Store.objects.annotate(
        order_count=Count('order', filter=Q(order__created_at__date__gte=start, order__created_at__date__lte=end)),
        revenue=Sum('order__total_amount', filter=Q(order__status__in=['delivered', 'completed'], order__created_at__date__gte=start, order__created_at__date__lte=end))
    ).order_by('-order_count')
    
    # User registrations
    new_users = User.objects.filter(
        date_joined__date__gte=start,
        date_joined__date__lte=end
    ).count()
    
    # Popular genres
    popular_genres = Book.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:10]
    
    context = {
        'start_date': start.isoformat(),
        'end_date': end.isoformat(),
        'total_revenue': total_revenue,
        'total_orders': orders.count(),
        'orders_by_store': orders_by_store,
        'new_users': new_users,
        'popular_genres': popular_genres,
    }
    return render(request, 'admin/reports.html', context)


@normal_admin_required
def dashboard_admin(request):
    """Dashboard for normal admins authenticated via name + reference number."""
    admin_account = request.normal_admin

    report_queryset = IssueReport.objects.all()
    pending_reports = report_queryset.filter(status=IssueReport.STATUS_PENDING).count()
    under_review_reports = report_queryset.filter(status=IssueReport.STATUS_UNDER_REVIEW).count()
    resolved_reports = report_queryset.filter(status=IssueReport.STATUS_RESOLVED).count()

    sub_admin_conversations = SupportConversation.objects.filter(
        target=SupportConversation.TARGET_SUB_ADMIN
    ).filter(
        Q(assigned_sub_admin=admin_account) | Q(assigned_sub_admin__isnull=True)
    )
    open_support_conversations = sub_admin_conversations.filter(status=SupportConversation.STATUS_OPEN).count()
    unread_support_messages = SupportMessage.objects.filter(
        conversation__in=sub_admin_conversations,
        is_read=False,
        sender_role__in=[IssueReport.ROLE_CUSTOMER, IssueReport.ROLE_STORE_OWNER],
    ).count()

    restricted_users_count = AccountRestriction.objects.filter(
        Q(is_suspended=True) | Q(is_deleted=True)
    ).count()

    context = {
        "admin_account": admin_account,
        "pending_reports": pending_reports,
        "under_review_reports": under_review_reports,
        "resolved_reports": resolved_reports,
        "open_support_conversations": open_support_conversations,
        "unread_support_messages": unread_support_messages,
        "restricted_users_count": restricted_users_count,
        "recent_reports": report_queryset.select_related('reporter', 'reported_user')[:6],
        "is_normal_admin": True,
    }
    return render(request, "admin/dashboard_admin.html", context)


def normal_admin_login_page(request):
    """Login page for normal admins (name + reference number)."""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard_super')

    admin_account = get_current_normal_admin(request)
    if admin_account:
        if admin_account.status == AdminAccount.STATUS_DELETED:
            clear_normal_admin_session(request)
            messages.error(request, "This Sub-Admin account has been deleted.")
        elif admin_account.is_currently_suspended():
            clear_normal_admin_session(request)
            until_text = ""
            if admin_account.suspension_until:
                until_text = timezone.localtime(admin_account.suspension_until).strftime('%Y-%m-%d %H:%M')
                until_text = f" until {until_text}"
            reason_text = admin_account.suspension_reason or "No reason was provided."
            messages.error(request, f"Sub-Admin account is suspended{until_text}. Reason: {reason_text}")
        else:
            return redirect('dashboard_admin')
    return render(request, "admin/login.html")


def admin_login(request):
    """Custom admin login view that redirects to admin dashboard."""
    clear_normal_admin_session(request)

    # This login is reserved for the Super Admin account.
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard_super')
        auth_logout(request)

    if request.method == "POST":
        username_or_email = (request.POST.get("username") or "").strip()
        password = request.POST.get("password")

        user = authenticate(request, username=username_or_email, password=password)

        # Allow login with email as hinted by the admin form placeholder.
        if user is None and "@" in username_or_email:
            matched_user = User.objects.filter(email__iexact=username_or_email).first()
            if matched_user:
                user = authenticate(request, username=matched_user.username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard_super')
            messages.error(request, "Only the Super Admin can access this login.")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "admin/login_admin.html")


def get_report_target_queryset(reporter_role):
    if reporter_role == CUSTOMER_GROUP:
        return User.objects.filter(
            Q(groups__name=STORE_OWNER_GROUP) | Q(owned_stores__isnull=False)
        ).exclude(is_superuser=True).distinct().order_by('username')
    return User.objects.filter(groups__name=CUSTOMER_GROUP).exclude(is_superuser=True).distinct().order_by('username')


@login_required
def issue_report_create(request):
    if request.user.is_superuser:
        messages.error(request, "Super Admin cannot create user issue reports.")
        return redirect('dashboard_super')

    reporter_role = get_user_role_for_platform(request.user)
    target_users = get_report_target_queryset(reporter_role).exclude(id=request.user.id)

    if request.method == "POST":
        reported_user_id = request.POST.get("reported_user")
        category = request.POST.get("category")
        description = (request.POST.get("description") or "").strip()
        attachment = request.FILES.get("attachment")

        if not reported_user_id or not category or not description:
            messages.error(request, "Reported user, category, and description are required.")
            return redirect('issue_report_create')

        reported_user = target_users.filter(id=reported_user_id).first()
        if not reported_user:
            messages.error(request, "Invalid reported user selected.")
            return redirect('issue_report_create')

        assigned_sub_admin = get_default_active_sub_admin()
        with transaction.atomic():
            report = IssueReport.objects.create(
                reporter=request.user,
                reporter_role=reporter_role,
                reported_user=reported_user,
                category=category,
                description=description,
                attachment=attachment,
                assigned_sub_admin=assigned_sub_admin,
            )
            support_conversation = seed_issue_report_support_thread(report)

        create_activity_log(
            action="issue_report_created",
            actor_role=reporter_role,
            actor_name=request.user.username,
            target_type="issue_report",
            target_identifier=f"report:{report.id}",
            metadata={
                "reported_user_id": reported_user.id,
                "category": category,
                "assigned_sub_admin_id": assigned_sub_admin.id if assigned_sub_admin else None,
            },
        )

        messages.success(
            request,
            "Issue report submitted. A support chat with Sub-Admin was created automatically.",
        )
        return redirect('support_chat_detail', conversation_id=support_conversation.id)

    context = {
        "report_categories": IssueReport.CATEGORY_CHOICES,
        "target_users": target_users,
        "reporter_role": reporter_role,
    }
    template_name = 'store/issue_report_form.html' if reporter_role == STORE_OWNER_GROUP else 'customer/issue_report_form.html'
    return render(request, template_name, context)


@login_required
def my_issue_reports(request):
    if request.user.is_superuser:
        return redirect('super_admin_issue_reports')

    reporter_role = get_user_role_for_platform(request.user)
    reports = IssueReport.objects.filter(
        reporter=request.user
    ).select_related('reported_user', 'assigned_sub_admin').order_by('-created_at')

    conversations = SupportConversation.objects.filter(
        user=request.user,
        issue_report__in=reports,
    ).select_related('issue_report').order_by('-updated_at')
    conversation_by_report = {}
    for conversation in conversations:
        if conversation.issue_report_id and conversation.issue_report_id not in conversation_by_report:
            conversation_by_report[conversation.issue_report_id] = conversation
    report_rows = [{"report": report, "conversation": conversation_by_report.get(report.id)} for report in reports]

    context = {
        "reports": reports,
        "report_rows": report_rows,
        "reporter_role": reporter_role,
    }
    template_name = 'store/my_issue_reports.html' if reporter_role == STORE_OWNER_GROUP else 'customer/my_issue_reports.html'
    return render(request, template_name, context)


@normal_admin_required
def sub_admin_issue_reports(request):
    reports = IssueReport.objects.select_related(
        'reporter',
        'reported_user',
        'assigned_sub_admin',
        'reviewed_by',
    ).order_by('-created_at')

    status_filter = (request.GET.get("status") or "").strip()
    assigned_filter = (request.GET.get("assigned") or "").strip()
    search_query = (request.GET.get("search") or "").strip()

    if status_filter:
        reports = reports.filter(status=status_filter)

    if assigned_filter == "mine":
        reports = reports.filter(assigned_sub_admin=request.normal_admin)
    elif assigned_filter == "unassigned":
        reports = reports.filter(assigned_sub_admin__isnull=True)

    if search_query:
        reports = reports.filter(
            Q(reporter__username__icontains=search_query)
            | Q(reported_user__username__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    context = {
        "reports": reports[:250],
        "status_filter": status_filter,
        "assigned_filter": assigned_filter,
        "search_query": search_query,
        "report_status_choices": IssueReport.STATUS_CHOICES,
        "pending_reports": IssueReport.objects.filter(status=IssueReport.STATUS_PENDING).count(),
        "under_review_reports": IssueReport.objects.filter(status=IssueReport.STATUS_UNDER_REVIEW).count(),
        "is_normal_admin": True,
        "admin_account": request.normal_admin,
    }
    return render(request, 'admin/sub_admin_issue_reports.html', context)


@normal_admin_required
@require_POST
def sub_admin_update_issue_report(request, report_id):
    report = get_object_or_404(IssueReport, id=report_id)
    new_status = (request.POST.get("status") or "").strip()
    resolution_note = (request.POST.get("resolution_note") or "").strip()
    escalate_to_admin = request.POST.get("escalate_to_admin") == "1"

    valid_statuses = {choice[0] for choice in IssueReport.STATUS_CHOICES}
    if new_status not in valid_statuses:
        messages.error(request, "Invalid report status selected.")
        return redirect('sub_admin_issue_reports')

    report.status = new_status
    report.reviewed_by = request.normal_admin
    report.reviewed_by_super_admin = None
    if not report.assigned_sub_admin:
        report.assigned_sub_admin = request.normal_admin

    if resolution_note:
        report.resolution_note = resolution_note

    if new_status in {IssueReport.STATUS_RESOLVED, IssueReport.STATUS_REJECTED}:
        report.resolved_at = timezone.now()
    else:
        report.resolved_at = None

    if escalate_to_admin:
        report.escalated_to_admin = True
        admin_conversation = get_or_create_issue_support_conversation(report, SupportConversation.TARGET_ADMIN)
        SupportMessage.objects.create(
            conversation=admin_conversation,
            sender_sub_admin=request.normal_admin,
            sender_role=SupportMessage.ROLE_SUB_ADMIN,
            content=build_sub_admin_escalation_message(
                report,
                request.normal_admin.name,
                resolution_note or "Issue report escalated for Super Admin review.",
            ),
            attachment=report.attachment if report.attachment else None,
            is_read=False,
        )

    report.save()

    create_activity_log(
        action="issue_report_status_updated",
        actor_role=ModerationActivityLog.ACTOR_SUB_ADMIN,
        actor_name=request.normal_admin.name,
        target_type="issue_report",
        target_identifier=f"report:{report.id}",
        reason=resolution_note,
        metadata={"status": new_status, "escalated_to_admin": report.escalated_to_admin},
    )

    messages.success(request, f"Issue report #{report.id} updated to {report.get_status_display()}.")
    return redirect('sub_admin_issue_reports')


@normal_admin_required
def sub_admin_manage_accounts(request):
    users = User.objects.filter(is_superuser=False).filter(
        Q(groups__name=CUSTOMER_GROUP) | Q(groups__name=STORE_OWNER_GROUP)
    ).distinct().order_by('-date_joined')

    role_filter = (request.GET.get("role") or "").strip()
    status_filter = (request.GET.get("status") or "").strip()
    search_query = (request.GET.get("search") or "").strip()

    if role_filter in {CUSTOMER_GROUP, STORE_OWNER_GROUP}:
        users = users.filter(groups__name=role_filter)

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
        )

    if status_filter == "active":
        users = users.filter(is_active=True)
    elif status_filter == "suspended":
        users = users.filter(account_restriction__is_suspended=True)
    elif status_filter == "deleted":
        users = users.filter(account_restriction__is_deleted=True)

    paginator = Paginator(users, 25)
    page_number = request.GET.get("page", 1)
    users_page = paginator.get_page(page_number)

    restrictions = AccountRestriction.objects.filter(user__in=users_page.object_list)
    restriction_map = {restriction.user_id: restriction for restriction in restrictions}
    user_rows = []
    for user_obj in users_page.object_list:
        restriction = restriction_map.get(user_obj.id)
        if user_obj.groups.filter(name=STORE_OWNER_GROUP).exists():
            role_value = STORE_OWNER_GROUP
        else:
            role_value = CUSTOMER_GROUP
        user_rows.append(
            {
                "user": user_obj,
                "role": role_value,
                "restriction": restriction,
            }
        )

    context = {
        "users_page": users_page,
        "user_rows": user_rows,
        "restriction_map": restriction_map,
        "role_filter": role_filter,
        "status_filter": status_filter,
        "search_query": search_query,
        "is_normal_admin": True,
        "admin_account": request.normal_admin,
    }
    return render(request, 'admin/sub_admin_account_management.html', context)


@normal_admin_required
@require_POST
def sub_admin_account_action(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_role = get_user_role_for_platform(target_user)
    action = (request.POST.get("action") or "").strip()
    reason = (request.POST.get("reason") or "").strip()
    next_url = request.POST.get("next") or reverse('sub_admin_manage_accounts')

    if target_user.is_superuser or target_role not in {CUSTOMER_GROUP, STORE_OWNER_GROUP}:
        messages.error(request, "Sub-Admin can only manage customer and store owner accounts.")
        return redirect(next_url)

    restriction = get_or_create_restriction(target_user)
    now = timezone.now()

    if action == "suspend":
        duration_days_raw = (request.POST.get("duration_days") or "7").strip()
        try:
            duration_days = max(1, int(duration_days_raw))
        except ValueError:
            duration_days = 7

        restriction.is_suspended = True
        restriction.suspended_reason = reason or "No reason was provided."
        restriction.suspended_until = now + timedelta(days=duration_days)
        restriction.save()

        target_user.is_active = False
        target_user.save(update_fields=['is_active'])

        notify_user_by_email(
            target_user,
            "BookHub account suspended",
            f"Your account has been suspended for {duration_days} day(s). Reason: {restriction.suspended_reason}",
        )

        create_activity_log(
            action="user_suspended",
            actor_role=ModerationActivityLog.ACTOR_SUB_ADMIN,
            actor_name=request.normal_admin.name,
            target_type=target_role,
            target_identifier=f"user:{target_user.id}:{target_user.username}",
            reason=restriction.suspended_reason,
            metadata={"duration_days": duration_days},
        )
        messages.success(request, f"{target_user.username} has been suspended.")

    elif action == "delete":
        deletion_reason = reason or "No reason was provided."
        restriction.is_deleted = True
        restriction.deleted_reason = deletion_reason
        restriction.is_suspended = False
        restriction.suspended_reason = ""
        restriction.suspended_until = None
        restriction.save()

        target_user.is_active = False
        target_user.save(update_fields=['is_active'])

        notify_user_by_email(
            target_user,
            "BookHub account deleted",
            f"Your account has been permanently deleted. Reason: {deletion_reason}",
        )

        create_activity_log(
            action="user_deleted",
            actor_role=ModerationActivityLog.ACTOR_SUB_ADMIN,
            actor_name=request.normal_admin.name,
            target_type=target_role,
            target_identifier=f"user:{target_user.id}:{target_user.username}",
            reason=deletion_reason,
        )
        messages.success(request, f"{target_user.username} has been permanently deleted.")

    elif action == "restore":
        if restriction.is_deleted:
            messages.error(request, "Deleted accounts cannot be restored by Sub-Admin.")
            return redirect(next_url)

        restriction.is_suspended = False
        restriction.suspended_reason = ""
        restriction.suspended_until = None
        restriction.save()

        if not restriction.is_deleted and not target_user.is_active:
            target_user.is_active = True
            target_user.save(update_fields=['is_active'])

        create_activity_log(
            action="user_restored",
            actor_role=ModerationActivityLog.ACTOR_SUB_ADMIN,
            actor_name=request.normal_admin.name,
            target_type=target_role,
            target_identifier=f"user:{target_user.id}:{target_user.username}",
        )
        messages.success(request, f"{target_user.username} has been restored.")
    else:
        messages.error(request, "Invalid account action.")

    return redirect(next_url)


@normal_admin_required
def sub_admin_activity_logs(request):
    logs = ModerationActivityLog.objects.filter(
        actor_role=ModerationActivityLog.ACTOR_SUB_ADMIN,
        actor_name=request.normal_admin.name,
    )[:300]
    context = {
        "logs": logs,
        "is_normal_admin": True,
        "admin_account": request.normal_admin,
    }
    return render(request, 'admin/sub_admin_activity_logs.html', context)


def get_sub_admin_conversation_scope(admin_account):
    return SupportConversation.objects.filter(target=SupportConversation.TARGET_SUB_ADMIN).filter(
        Q(assigned_sub_admin=admin_account) | Q(assigned_sub_admin__isnull=True)
    )


def resolve_support_viewer(request, conversation):
    if request.user.is_authenticated and conversation.user_id == request.user.id:
        return {"viewer_kind": "user", "admin_account": None}

    normal_admin = get_current_normal_admin(request)
    if normal_admin and normal_admin.status == AdminAccount.STATUS_ACTIVE and not normal_admin.is_currently_suspended():
        if conversation.target == SupportConversation.TARGET_SUB_ADMIN and (
            conversation.assigned_sub_admin_id in (None, normal_admin.id)
        ):
            if conversation.assigned_sub_admin_id is None:
                conversation.assigned_sub_admin = normal_admin
                conversation.save(update_fields=['assigned_sub_admin', 'updated_at'])
            return {"viewer_kind": "sub_admin", "admin_account": normal_admin}

    if request.user.is_authenticated and request.user.is_superuser:
        return {"viewer_kind": "admin", "admin_account": None}

    return None


def mark_support_messages_as_read(conversation, viewer_kind):
    if viewer_kind == "user":
        conversation.messages.filter(
            is_read=False,
            sender_role__in=[SupportMessage.ROLE_SUB_ADMIN, SupportMessage.ROLE_ADMIN],
        ).update(is_read=True)
    elif viewer_kind == "sub_admin":
        conversation.messages.filter(
            is_read=False,
            sender_role__in=[IssueReport.ROLE_CUSTOMER, IssueReport.ROLE_STORE_OWNER],
        ).update(is_read=True)
    elif viewer_kind == "admin":
        conversation.messages.filter(
            is_read=False,
            sender_role__in=[IssueReport.ROLE_CUSTOMER, IssueReport.ROLE_STORE_OWNER, SupportMessage.ROLE_SUB_ADMIN],
        ).update(is_read=True)


def serialize_support_message(message_obj, viewer_kind, request):
    is_me = False
    current_sub_admin = get_current_normal_admin(request)

    if viewer_kind == "user" and request.user.is_authenticated:
        is_me = message_obj.sender_user_id == request.user.id
    elif viewer_kind == "sub_admin" and current_sub_admin:
        is_me = message_obj.sender_sub_admin_id == current_sub_admin.id
    elif viewer_kind == "admin":
        is_me = message_obj.sender_role == SupportMessage.ROLE_ADMIN

    attachment_url = message_obj.attachment.url if message_obj.attachment else ""
    attachment_name = os.path.basename(message_obj.attachment.name) if message_obj.attachment else ""

    return {
        "id": message_obj.id,
        "sender_name": get_support_sender_name(message_obj),
        "sender_role": message_obj.sender_role,
        "content": message_obj.content,
        "created_at": timezone.localtime(message_obj.created_at).strftime('%Y-%m-%d %H:%M'),
        "attachment_url": attachment_url,
        "attachment_name": attachment_name,
        "attachment_is_image": is_image_attachment(message_obj.attachment),
        "is_read": message_obj.is_read,
        "is_me": is_me,
    }


@login_required
def support_chat_list(request):
    if request.user.is_superuser:
        return redirect('super_admin_support_chat_list')

    user_role = get_user_role_for_platform(request.user)
    conversations = SupportConversation.objects.filter(user=request.user).select_related(
        'assigned_sub_admin',
        'issue_report',
    ).order_by('-updated_at')

    search_query = (request.GET.get("search") or "").strip()
    if search_query:
        conversations = conversations.filter(
            Q(subject__icontains=search_query)
            | Q(messages__content__icontains=search_query)
        ).distinct()

    conversation_rows = []
    total_unread = 0
    for conversation in conversations:
        last_message = conversation.messages.order_by('-created_at').first()
        unread_count = conversation.messages.filter(
            is_read=False,
            sender_role__in=[SupportMessage.ROLE_SUB_ADMIN, SupportMessage.ROLE_ADMIN],
        ).count()
        total_unread += unread_count
        conversation_rows.append(
            {
                "conversation": conversation,
                "last_message": last_message,
                "unread_count": unread_count,
            }
        )

    context = {
        "conversation_rows": conversation_rows,
        "total_unread": total_unread,
        "search_query": search_query,
        "target_choices": SupportConversation.TARGET_CHOICES,
        "open_reports": IssueReport.objects.filter(
            reporter=request.user
        ).exclude(status__in=[IssueReport.STATUS_RESOLVED, IssueReport.STATUS_REJECTED])[:20],
    }
    template_name = 'store/support_chat_list.html' if user_role == STORE_OWNER_GROUP else 'customer/support_chat_list.html'
    return render(request, template_name, context)


@login_required
@require_POST
def support_chat_start(request):
    if request.user.is_superuser:
        return redirect('super_admin_support_chat_list')

    user_role = get_user_role_for_platform(request.user)
    target = (request.POST.get("target") or SupportConversation.TARGET_SUB_ADMIN).strip()
    subject = (request.POST.get("subject") or "").strip()
    issue_report_id = (request.POST.get("issue_report_id") or "").strip()
    message_text = (request.POST.get("message") or "").strip()
    attachment = request.FILES.get("attachment")

    if target not in {SupportConversation.TARGET_SUB_ADMIN, SupportConversation.TARGET_ADMIN}:
        target = SupportConversation.TARGET_SUB_ADMIN

    issue_report = None
    if issue_report_id:
        issue_report = IssueReport.objects.filter(id=issue_report_id, reporter=request.user).first()
        if not issue_report:
            messages.error(request, "Invalid issue report selected.")
            return redirect('support_chat_list')

    conversation = SupportConversation.objects.create(
        user=request.user,
        user_role=user_role,
        issue_report=issue_report,
        subject=subject,
        assigned_sub_admin=(
            issue_report.assigned_sub_admin
            if issue_report and target == SupportConversation.TARGET_SUB_ADMIN
            else get_default_active_sub_admin() if target == SupportConversation.TARGET_SUB_ADMIN else None
        ),
        target=target,
    )

    if message_text or attachment:
        SupportMessage.objects.create(
            conversation=conversation,
            sender_user=request.user,
            sender_role=user_role,
            content=message_text,
            attachment=attachment,
        )

    create_activity_log(
        action="support_chat_started",
        actor_role=user_role,
        actor_name=request.user.username,
        target_type="support_chat",
        target_identifier=f"conversation:{conversation.id}",
        metadata={"target": target, "issue_report_id": issue_report.id if issue_report else None},
    )

    return redirect('support_chat_detail', conversation_id=conversation.id)


@login_required
def support_chat_detail(request, conversation_id):
    conversation = get_object_or_404(
        SupportConversation.objects.select_related('assigned_sub_admin'),
        id=conversation_id,
        user=request.user,
    )
    mark_support_messages_as_read(conversation, "user")
    messages_qs = conversation.messages.select_related('sender_user', 'sender_sub_admin')

    user_role = get_user_role_for_platform(request.user)
    context = {
        "conversation": conversation,
        "messages_list": messages_qs,
        "viewer_kind": "user",
    }
    template_name = 'store/support_chat_detail.html' if user_role == STORE_OWNER_GROUP else 'customer/support_chat_detail.html'
    return render(request, template_name, context)


@normal_admin_required
def sub_admin_support_chat_list(request):
    conversations = get_sub_admin_conversation_scope(request.normal_admin).select_related(
        'user',
        'issue_report',
        'assigned_sub_admin',
    ).order_by('-updated_at')

    search_query = (request.GET.get("search") or "").strip()
    if search_query:
        conversations = conversations.filter(
            Q(user__username__icontains=search_query)
            | Q(subject__icontains=search_query)
            | Q(messages__content__icontains=search_query)
        ).distinct()

    conversation_rows = []
    total_unread = 0
    for conversation in conversations:
        unread_count = conversation.messages.filter(
            is_read=False,
            sender_role__in=[IssueReport.ROLE_CUSTOMER, IssueReport.ROLE_STORE_OWNER],
        ).count()
        total_unread += unread_count
        conversation_rows.append(
            {
                "conversation": conversation,
                "last_message": conversation.messages.order_by('-created_at').first(),
                "unread_count": unread_count,
            }
        )

    context = {
        "conversation_rows": conversation_rows,
        "total_unread": total_unread,
        "search_query": search_query,
        "is_normal_admin": True,
        "admin_account": request.normal_admin,
    }
    return render(request, 'admin/sub_admin_support_chat_list.html', context)


@normal_admin_required
def sub_admin_support_chat_detail(request, conversation_id):
    conversation = get_object_or_404(get_sub_admin_conversation_scope(request.normal_admin), id=conversation_id)
    if conversation.assigned_sub_admin_id is None:
        conversation.assigned_sub_admin = request.normal_admin
        conversation.save(update_fields=['assigned_sub_admin', 'updated_at'])

    mark_support_messages_as_read(conversation, "sub_admin")
    messages_qs = conversation.messages.select_related('sender_user', 'sender_sub_admin')

    context = {
        "conversation": conversation,
        "messages_list": messages_qs,
        "viewer_kind": "sub_admin",
        "is_normal_admin": True,
        "admin_account": request.normal_admin,
    }
    return render(request, 'admin/sub_admin_support_chat_detail.html', context)


@normal_admin_required
@require_POST
def sub_admin_escalate_support_chat(request, conversation_id):
    conversation = get_object_or_404(get_sub_admin_conversation_scope(request.normal_admin), id=conversation_id)

    escalation_text = build_sub_admin_escalation_message(
        conversation.issue_report,
        request.normal_admin.name,
        "Support chat escalated to Super Admin.",
    )
    SupportMessage.objects.create(
        conversation=conversation,
        sender_sub_admin=request.normal_admin,
        sender_role=SupportMessage.ROLE_SUB_ADMIN,
        content=escalation_text,
        attachment=conversation.issue_report.attachment if conversation.issue_report and conversation.issue_report.attachment else None,
        is_read=False,
    )

    conversation.target = SupportConversation.TARGET_ADMIN
    conversation.save(update_fields=['target', 'updated_at'])
    if conversation.issue_report and not conversation.issue_report.escalated_to_admin:
        conversation.issue_report.escalated_to_admin = True
        conversation.issue_report.save(update_fields=['escalated_to_admin', 'updated_at'])

    create_activity_log(
        action="support_chat_escalated",
        actor_role=ModerationActivityLog.ACTOR_SUB_ADMIN,
        actor_name=request.normal_admin.name,
        target_type="support_chat",
        target_identifier=f"conversation:{conversation.id}",
    )

    messages.success(request, f"Support chat #{conversation.id} escalated to Admin.")
    return redirect('sub_admin_support_chat_list')


@require_POST
def support_chat_send_message(request, conversation_id):
    conversation = get_object_or_404(SupportConversation, id=conversation_id)
    viewer_context = resolve_support_viewer(request, conversation)

    if not viewer_context:
        return JsonResponse({"success": False, "error": "Permission denied"}, status=403)

    content = (request.POST.get("content") or "").strip()
    attachment = request.FILES.get("attachment")
    if not content and not attachment:
        return JsonResponse({"success": False, "error": "Message cannot be empty."}, status=400)

    sender_user = None
    sender_sub_admin = None
    sender_role = SupportMessage.ROLE_ADMIN
    viewer_kind = viewer_context["viewer_kind"]

    if viewer_kind == "user":
        sender_user = request.user
        sender_role = conversation.user_role
    elif viewer_kind == "sub_admin":
        sender_sub_admin = viewer_context["admin_account"]
        sender_role = SupportMessage.ROLE_SUB_ADMIN
    elif viewer_kind == "admin":
        sender_user = request.user
        sender_role = SupportMessage.ROLE_ADMIN

    message_obj = SupportMessage.objects.create(
        conversation=conversation,
        sender_user=sender_user,
        sender_sub_admin=sender_sub_admin,
        sender_role=sender_role,
        content=content,
        attachment=attachment,
        is_read=False,
    )

    conversation.save()

    return JsonResponse(
        {
            "success": True,
            "message": serialize_support_message(message_obj, viewer_kind, request),
        }
    )


@require_GET
def support_chat_poll_messages(request, conversation_id):
    conversation = get_object_or_404(SupportConversation, id=conversation_id)
    viewer_context = resolve_support_viewer(request, conversation)

    if not viewer_context:
        return JsonResponse({"success": False, "error": "Permission denied"}, status=403)

    viewer_kind = viewer_context["viewer_kind"]
    try:
        last_id = int(request.GET.get("last_id", "0"))
    except ValueError:
        last_id = 0

    new_messages = conversation.messages.select_related('sender_user', 'sender_sub_admin').filter(id__gt=last_id)
    payload = [serialize_support_message(message_obj, viewer_kind, request) for message_obj in new_messages]

    mark_support_messages_as_read(conversation, viewer_kind)

    if viewer_kind == "user":
        unread_count = conversation.messages.filter(
            is_read=False,
            sender_role__in=[SupportMessage.ROLE_SUB_ADMIN, SupportMessage.ROLE_ADMIN],
        ).count()
    elif viewer_kind == "sub_admin":
        unread_count = conversation.messages.filter(
            is_read=False,
            sender_role__in=[IssueReport.ROLE_CUSTOMER, IssueReport.ROLE_STORE_OWNER],
        ).count()
    else:
        unread_count = conversation.messages.filter(
            is_read=False,
            sender_role__in=[IssueReport.ROLE_CUSTOMER, IssueReport.ROLE_STORE_OWNER, SupportMessage.ROLE_SUB_ADMIN],
        ).count()

    return JsonResponse(
        {
            "success": True,
            "messages": payload,
            "unread_count": unread_count,
        }
    )


@super_admin_required
def super_admin_support_chat_list(request):
    conversations = SupportConversation.objects.filter(
        target=SupportConversation.TARGET_ADMIN
    ).select_related('user', 'issue_report', 'assigned_sub_admin').order_by('-updated_at')

    search_query = (request.GET.get("search") or "").strip()
    if search_query:
        conversations = conversations.filter(
            Q(user__username__icontains=search_query)
            | Q(subject__icontains=search_query)
            | Q(messages__content__icontains=search_query)
        ).distinct()

    conversation_rows = []
    total_unread = 0
    for conversation in conversations:
        unread_count = conversation.messages.filter(
            is_read=False,
            sender_role__in=[IssueReport.ROLE_CUSTOMER, IssueReport.ROLE_STORE_OWNER, SupportMessage.ROLE_SUB_ADMIN],
        ).count()
        total_unread += unread_count
        conversation_rows.append(
            {
                "conversation": conversation,
                "last_message": conversation.messages.order_by('-created_at').first(),
                "unread_count": unread_count,
            }
        )

    context = {
        "conversation_rows": conversation_rows,
        "total_unread": total_unread,
        "search_query": search_query,
    }
    return render(request, 'admin/super_admin_support_chat_list.html', context)


@super_admin_required
def super_admin_support_chat_detail(request, conversation_id):
    conversation = get_object_or_404(SupportConversation, id=conversation_id, target=SupportConversation.TARGET_ADMIN)
    mark_support_messages_as_read(conversation, "admin")
    messages_qs = conversation.messages.select_related('sender_user', 'sender_sub_admin')

    context = {
        "conversation": conversation,
        "messages_list": messages_qs,
        "viewer_kind": "admin",
    }
    return render(request, 'admin/super_admin_support_chat_detail.html', context)


@super_admin_required
def super_admin_issue_reports(request):
    reports = IssueReport.objects.select_related(
        'reporter',
        'reported_user',
        'assigned_sub_admin',
        'reviewed_by',
    ).order_by('-created_at')

    status_filter = (request.GET.get("status") or "").strip()
    search_query = (request.GET.get("search") or "").strip()
    if status_filter:
        reports = reports.filter(status=status_filter)
    if search_query:
        reports = reports.filter(
            Q(reporter__username__icontains=search_query)
            | Q(reported_user__username__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    context = {
        "reports": reports[:300],
        "status_filter": status_filter,
        "search_query": search_query,
        "sub_admins": AdminAccount.objects.exclude(status=AdminAccount.STATUS_DELETED).order_by('name'),
        "report_status_choices": IssueReport.STATUS_CHOICES,
    }
    return render(request, 'admin/super_admin_issue_reports.html', context)


@super_admin_required
@require_POST
def super_admin_update_issue_report(request, report_id):
    report = get_object_or_404(IssueReport, id=report_id)
    new_status = (request.POST.get("status") or "").strip()
    resolution_note = (request.POST.get("resolution_note") or "").strip()

    valid_statuses = {choice[0] for choice in IssueReport.STATUS_CHOICES}
    if new_status not in valid_statuses:
        messages.error(request, "Invalid report status selected.")
        return redirect('super_admin_issue_reports')

    report.status = new_status
    report.reviewed_by = None
    report.reviewed_by_super_admin = request.user
    if resolution_note:
        report.resolution_note = resolution_note
    report.resolved_at = timezone.now() if new_status in {IssueReport.STATUS_RESOLVED, IssueReport.STATUS_REJECTED} else None
    report.save()

    create_activity_log(
        action="issue_report_status_updated",
        actor_role=ModerationActivityLog.ACTOR_ADMIN,
        actor_name=request.user.username,
        target_type="issue_report",
        target_identifier=f"report:{report.id}",
        reason=resolution_note,
        metadata={"status": new_status},
    )

    messages.success(request, f"Issue report #{report.id} updated.")
    return redirect('super_admin_issue_reports')


@super_admin_required
@require_POST
def super_admin_reassign_issue_report(request, report_id):
    report = get_object_or_404(IssueReport, id=report_id)
    sub_admin_id = (request.POST.get("sub_admin_id") or "").strip()

    if sub_admin_id:
        sub_admin = get_object_or_404(AdminAccount, id=sub_admin_id)
        if sub_admin.status == AdminAccount.STATUS_DELETED:
            messages.error(request, "Cannot assign report to a deleted Sub-Admin.")
            return redirect('super_admin_issue_reports')
        report.assigned_sub_admin = sub_admin
    else:
        report.assigned_sub_admin = None
    report.save(update_fields=['assigned_sub_admin', 'updated_at'])

    create_activity_log(
        action="issue_report_reassigned",
        actor_role=ModerationActivityLog.ACTOR_ADMIN,
        actor_name=request.user.username,
        target_type="issue_report",
        target_identifier=f"report:{report.id}",
        metadata={"assigned_sub_admin_id": report.assigned_sub_admin_id},
    )

    messages.success(request, f"Issue report #{report.id} reassigned successfully.")
    return redirect('super_admin_issue_reports')


@super_admin_required
def super_admin_sub_admin_controls(request):
    admins = AdminAccount.objects.all().order_by('-created_at')
    search_query = (request.GET.get("search") or "").strip()
    if search_query:
        admins = admins.filter(
            Q(name__icontains=search_query)
            | Q(admin_type__icontains=search_query)
            | Q(ref_number__icontains=search_query)
        )

    logs = ModerationActivityLog.objects.filter(
        actor_role__in=[ModerationActivityLog.ACTOR_SUB_ADMIN, ModerationActivityLog.ACTOR_ADMIN]
    )[:150]

    context = {
        "admins": admins,
        "logs": logs,
        "search_query": search_query,
    }
    return render(request, 'admin/super_admin_sub_admin_controls.html', context)


@super_admin_required
@require_POST
def super_admin_sub_admin_action(request, admin_id):
    admin_account = get_object_or_404(AdminAccount, id=admin_id)
    action = (request.POST.get("action") or "").strip()
    reason = (request.POST.get("reason") or "").strip()
    next_url = request.POST.get("next") or reverse('super_admin_sub_admin_controls')

    if action == "suspend":
        duration_days_raw = (request.POST.get("duration_days") or "7").strip()
        try:
            duration_days = max(1, int(duration_days_raw))
        except ValueError:
            duration_days = 7

        admin_account.status = AdminAccount.STATUS_SUSPENDED
        admin_account.suspension_reason = reason or "No reason was provided."
        admin_account.suspension_until = timezone.now() + timedelta(days=duration_days)
        admin_account.save(update_fields=['status', 'suspension_reason', 'suspension_until'])
        messages.success(request, f"{admin_account.name} has been suspended.")

        create_activity_log(
            action="sub_admin_suspended",
            actor_role=ModerationActivityLog.ACTOR_ADMIN,
            actor_name=request.user.username,
            target_type="sub_admin",
            target_identifier=f"admin_account:{admin_account.id}:{admin_account.name}",
            reason=admin_account.suspension_reason,
            metadata={"duration_days": duration_days},
        )

    elif action == "restore":
        admin_account.status = AdminAccount.STATUS_ACTIVE
        admin_account.suspension_reason = ""
        admin_account.suspension_until = None
        admin_account.save(update_fields=['status', 'suspension_reason', 'suspension_until'])
        messages.success(request, f"{admin_account.name} has been restored.")

        create_activity_log(
            action="sub_admin_restored",
            actor_role=ModerationActivityLog.ACTOR_ADMIN,
            actor_name=request.user.username,
            target_type="sub_admin",
            target_identifier=f"admin_account:{admin_account.id}:{admin_account.name}",
        )

    elif action == "delete":
        delete_reason = reason or "No reason was provided."
        admin_account.status = AdminAccount.STATUS_DELETED
        admin_account.suspension_reason = delete_reason
        admin_account.suspension_until = None
        admin_account.save(update_fields=['status', 'suspension_reason', 'suspension_until'])
        messages.success(request, f"{admin_account.name} has been permanently deleted.")

        create_activity_log(
            action="sub_admin_deleted",
            actor_role=ModerationActivityLog.ACTOR_ADMIN,
            actor_name=request.user.username,
            target_type="sub_admin",
            target_identifier=f"admin_account:{admin_account.id}:{admin_account.name}",
            reason=delete_reason,
        )
    else:
        messages.error(request, "Invalid Sub-Admin action.")

    return redirect(next_url)
