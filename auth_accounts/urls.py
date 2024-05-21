from django.urls import path, include
from .views import *
# from .utils import verify_email, reset_password

urlpatterns = [
    path("dummy_check", dummy_check, name="dummy-check"),
    path('register/', account_register, name='account-register'),
    path('verify_registration_email/<uidb64>/<token>/', verify_email, name='verify_registration_email'),

    
    path('forgot_password/', forgot_password, name='forgot_password'),
    # path('reset_password/<int:uid>/<str:token>/', reset_password, name='reset_password'),
    path('reset_password/<str:uidb64>/<str:token>/', reset_password, name='reset_password'),


    path('login/', account_login, name='account-login'),
    path('logout/', account_logout, name='account-logout'),

]