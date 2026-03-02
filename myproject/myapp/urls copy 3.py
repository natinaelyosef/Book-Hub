from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
        path('counter/', views.counter, name='counter'),
        path('register/', views.register, name='register'),
        path('login/', views.login_view, name='login'),
        path('logout/', views.logout, name='logout'),
        path('post/<int:pk>',views.post, name="post")
        ,
        path('store/', views.store, name='store'),

        path('store/registration/', views.store_registration, name='store_registration'),

        path('store/add_book/', views.add_book, name='add_book'),
        path('store/add_block/', views.add_book, name='add_block'),






       
        path('store/dashboard/', views.store_dashboard, name='store_dashboard'),
        path('store/add_book_registration/', views.add_book_registration, name='add_book_registration'),
        path('store/view_inventory/', views.view_inventory, name='view_inventory'),



       # path('<int:id>/', views.edit_book, name='edit_book'),
        path('store/delete/<int:id>/', views.book_delete, name='book_delete'),
        path('store/edit_book/<int:id>/', views.edit_book, name='edit_book'),  



        #store registration view and edit   and  delete
        path('store/registration/view/', views.store_registration_view, name='store_registration_view'),
        path('store/registration/edit/<int:id>/', views.edit_store, name='edit_store'),
        path('store/registration/delete/<int:id>/', views.delete_store, name='delete_store'),
                
           #customer dashboard     
           path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('stores/', views.store_list, name='store_list'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('cart/rent/<int:book_id>/', views.add_to_cart_rent, name='add_to_cart_rent'),
    path('cart/buy/<int:book_id>/', views.add_to_cart_buy, name='add_to_cart_buy'),
    path('cart/remove/<int:book_id>/<str:item_type>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.shopping_cart, name='shopping_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process_order, name='process_order'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),
    path('customer/orders/', views.order_history, name='order_history'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('quick-search/', views.quick_search, name='quick_search'),


] 