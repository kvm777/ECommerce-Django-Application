from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_home, name='admin-home'),
    path('products/', admin_products, name='admin-products'),
    path('users/', admin_users, name='admin-users'),

    # products 
    path('add-product/', addOrUpdateProduct, name='add-product'),
    path('update-product/<int:product_id>/', addOrUpdateProduct, name='update-product'),
    path('delete-product/<int:product_id>/', deleteProduct, name='delete-product'),

    # orders
    path('orders/', admin_orders, name='admin-orders'),
    
]