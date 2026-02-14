from django.db.models import Q

from .models import Order, Store

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
        if is_store_owner and stores.exists():
            context['pending_orders_count'] = Order.objects.filter(store__in=stores, status='pending').count()
            context['is_store_owner'] = True
    
    return context
