from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.views import View

from store.models import *
from .forms import *
# Create your views here.

def is_superuser(user):
    return user.is_superuser

# here i`m giving name for login-url


# @login_required(login_url='/')
@user_passes_test(is_superuser, login_url='account-login')
def admin_home(request):
    return render(request, 'admin_access/admin_home.html')


@user_passes_test(is_superuser, login_url='account-login')
def admin_users(request):
    customers = Customer.objects.all()
    context = {"customers":customers}
    return render(request, 'admin_access/admin_users.html', context)


@user_passes_test(is_superuser, login_url='account-login')
def admin_products(request):
    products = Product.objects.all()
    context = {"products":products}
    return render(request, 'admin_access/admin_products.html', context)


@user_passes_test(is_superuser, login_url='account-login')
def addOrUpdateProduct(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, id = product_id)
    else:
        product = None
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin-products'))
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_access/product_form.html', {'productform':form})


@user_passes_test(is_superuser, login_url='account-login')
def deleteProduct(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    product.delete()
    return redirect(reverse('admin-products'))


def admin_orders(request, customer_id=None):
    customers = Customer.objects.all()
    if customer_id:
        orders = Order.objects.filter(customer = customer_id )
    else:
        orders = Order.objects.all()
    return render(request, 'admin_access/admin_orders.html', {'orders':orders, 'customers':customers,})




