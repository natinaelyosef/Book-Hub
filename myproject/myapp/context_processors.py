from django.db.models import Q
from urllib.parse import quote_plus

from .models import AdminAccount, Order, Store, UserProfile


def _build_ui_avatar(name, background="4361ee"):
    safe_name = quote_plus(name or "User")
    return f"https://ui-avatars.com/api/?name={safe_name}&background={background}&color=fff&size=128&bold=true"

def store_context(request):
    """
    Context processor to provide store-related data to all templates.
    """
    context = {}
    if request.user.is_authenticated:
        store_filter = Q(owner_full_name__iexact=request.user.username)
        if request.user.email:
            store_filter |= Q(email__iexact=request.user.email.strip())

        stores = Store.objects.filter(store_filter).distinct()
        is_store_owner = request.user.is_superuser or request.user.groups.filter(name='store_owner').exists()

        # compute a display name for the account (typically owner name)
        # prefer the full name of the primary store owner if available
        account_owner = None
        if stores.exists():
            primary = stores.first()
            account_owner = getattr(primary, 'owner_full_name', None) or ''
        if not account_owner:
            account_owner = request.user.get_full_name().strip() or request.user.username
        context['account_owner'] = account_owner

        if is_store_owner and stores.exists():
            context['pending_orders_count'] = Order.objects.filter(store__in=stores, status='pending').count()
            context['is_store_owner'] = True

    current_normal_admin = None
    normal_admin_id = request.session.get("normal_admin_id")
    if normal_admin_id:
        current_normal_admin = AdminAccount.objects.filter(id=normal_admin_id).first()

    current_display_name = "Guest"
    current_role_label = "Guest"
    current_avatar_url = _build_ui_avatar("Guest")

    if current_normal_admin:
        current_display_name = current_normal_admin.name or "Sub Admin"
        current_role_label = "Sub-Admin"
        if current_normal_admin.profile_image:
            current_avatar_url = current_normal_admin.profile_image.url
        else:
            current_avatar_url = _build_ui_avatar(current_display_name, background="5b4cff")
    elif request.user.is_authenticated:
        current_display_name = request.user.get_username()
        current_role_label = "Super Admin" if request.user.is_superuser else "User"
        profile = UserProfile.objects.filter(user=request.user).first()
        if profile and profile.avatar:
            current_avatar_url = profile.avatar.url
        else:
            bg_color = "5b4cff" if request.user.is_superuser else "4361ee"
            current_avatar_url = _build_ui_avatar(current_display_name, background=bg_color)

    context.update(
        {
            "current_normal_admin": current_normal_admin,
            "current_avatar_url": current_avatar_url,
            "current_display_name": current_display_name,
            "current_role_label": current_role_label,
        }
    )

    return context
