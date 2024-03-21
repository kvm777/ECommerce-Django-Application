from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_home, name='admin-home'),
    path('products/', admin_products, name='admin-products'),
    path('users/', admin_users, name='admin-users'),

    # orders
    path('orders/', admin_orders, name='admin-orders'),
    path('orders/<int:customer_id>/', admin_orders, name='admin-orders-filtered'),

    # products 
    path('add-product/', addOrUpdateProduct, name='add-product'),
    path('update-product/<int:product_id>/', addOrUpdateProduct, name='update-product'),
    path('delete-product/<int:product_id>/', deleteProduct, name='delete-product'),

]