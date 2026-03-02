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
 


] 