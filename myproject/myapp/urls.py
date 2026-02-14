from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.index, name='index'),
    path('counter/', views.counter, name='counter'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('post/<int:pk>', views.post, name="post"),
    
    # Store registration
    path('store/', views.store, name='store'),
    path('store/registration/', views.store_registration, name='store_registration'),
    
    # Store dashboard and management
    path('store/dashboard/', views.store_dashboard, name='store_dashboard'),
    
    # Book management
    path('store/add_book/', views.add_book, name='add_book'),
    path('store/add_block/', views.add_book, name='add_block'),
    path('store/add_book_registration/', views.add_book_registration, name='add_book_registration'),
    path('store/view_inventory/', views.view_inventory, name='view_inventory'),
    path('store/delete/<int:id>/', views.book_delete, name='book_delete'),
    path('store/edit_book/<int:id>/', views.edit_book, name='edit_book'),
    path('store/manage-books/', views.manage_books, name='manage_books'),
    path('update-book-availability/', views.update_book_availability, name='update_book_availability'),
    
    # Store registration view, edit and delete
    path('store/registration/view/', views.store_registration_view, name='store_registration_view'),
    path('store/registration/edit/<int:id>/', views.edit_store, name='edit_store'),
    path('store/registration/delete/<int:id>/', views.delete_store, name='delete_store'),
    
    # Store Owner Order Management
    path('store/orders/', views.store_orders, name='store_orders'),
    path('store/orders/history/', views.store_order_history, name='store_order_history'),
    path('store/order/<int:order_id>/', views.store_order_detail, name='store_order_detail'),
   # path('store/order/process/<int:order_id>/', views.process_order, name='process_order'),
    path('store/order/process/<int:order_id>/', views.process_order, name='process_order'),
    path('store/delivery/update/<int:delivery_id>/', views.update_delivery_location, name='update_delivery_location'),
    path('store/wishlist/', views.store_wishlist, name='store_wishlist'),
    
    # Customer dashboard and browsing
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('stores/', views.store_list, name='store_list'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    
    # Quick Search API
    path('quick-search/', views.quick_search, name='quick_search'),
    
    # Shopping Cart URLs
    path('cart/rent/<int:book_id>/', views.add_to_cart_rent, name='add_to_cart_rent'),
    path('cart/buy/<int:book_id>/', views.add_to_cart_buy, name='add_to_cart_buy'),
    path('cart/remove/<int:book_id>/<str:item_type>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.shopping_cart, name='shopping_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    
    # Wishlist URLs
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/clear/', views.clear_wishlist, name='wishlist_clear_all'),
    
    # Customer Order Flow URLs
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.checkout, name='checkout_process'),
    path('create-order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/finish/<int:order_id>/', views.mark_order_finished, name='mark_order_finished'),
    path('order/track/<int:order_id>/', views.track_order, name='track_order'),
    path('customer/orders/history/', views.order_history, name='customer_order_history'),
    path('orders/history/', views.order_history, name='order_history'),
    path('order/review/<int:order_id>/', views.add_review, name='add_review'),
    
    # Customer Profile
    path('customer/profile/', views.customer_profile, name='customer_profile'),
]
