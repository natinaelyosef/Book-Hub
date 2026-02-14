from .models import Order, Store

def store_context(request):
    """
    Context processor to provide store-related data to all templates.
    """
    context = {}
    if request.user.is_authenticated:
        # Check if user owns any stores
        stores = Store.objects.filter(owner_full_name=request.user.username)
        if stores.exists():
            # Get pending orders count
            pending_orders_count = Order.objects.filter(store__in=stores, status='pending').count()
            context['pending_orders_count'] = pending_orders_count
            context['is_store_owner'] = True
    
    return context
