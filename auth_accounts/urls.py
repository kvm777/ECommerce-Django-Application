from django.urls import path
from .views import *

urlpatterns = [
    path('login/', account_login, name='account-login'),
    path('register/', account_register, name='account-register'),
    path('logout/', account_logout, name='account-logout'),
]