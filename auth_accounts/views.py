from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate

from store.models import Customer

# Create your views here.


def account_register(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "username already taken")
                return redirect(reverse("account-register"))
            elif User.objects.filter(email = email).exists():
                messages.error(request, "email already taken")
                return redirect(reverse("account-register"))
            else:
                user = User.objects.create_user(username=username, first_name = first_name ,last_name = last_name, password=password1, email = email)
                customer = Customer.objects.create(user = user, name = f"{first_name} {last_name}", email = email)
                user.save()
                return redirect(reverse("store"))
        else:
            messages.error(request, "password didn`t match")
            return redirect(reverse("account-register"))
        
    return render(request, "auth_accounts/register.html",{"page":"regiser page"})



def account_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username= username, password= password)

        if user != None:
            login(request, user)
            return redirect(reverse("store"))
        else:
            messages.info(request, "invalid crediantials")
    
    return render(request, 'auth_accounts/login.html')


def account_logout(request):
    logout(request)
    return redirect(reverse("store"))

