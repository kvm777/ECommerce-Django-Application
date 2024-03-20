from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
import datetime
from .utils import cartData, cookieCart, guestOrder

# Create your views here.

def store(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer = customer, complete = False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_quantity
    #     print(cartItems)

    # else:
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']
    #     order = cookieData['order']
    #     items = cookieData['items']



    # updated to maintain DRY(dont repeate yourself...)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'items':items, 'cartItems':cartItems}
    return render(request,'store/store.html', context)

def cart(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer = customer, complete = False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_quantity
    #     print(cartItems)

    # else:
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']
    #     order = cookieData['order']
    #     items = cookieData['items']


    # updated to maintain DRY(dont repeate yourself...)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = { 'items':items, 'order':order,'cartItems': cartItems }
    return render(request,'store/cart.html', context)


def checkout(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer = customer, complete = False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_quantity
    #     print(cartItems)

    # else:
    #     cookieData = cookieCart(request)
    #     cartItems = cookieData['cartItems']
    #     order = cookieData['order']
    #     items = cookieData['items']


    # updated to maintain DRY(dont repeate yourself...)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = { 'items':items, 'order':order, 'cartItems': cartItems } 
    return render(request,'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']
    # print(productId, action)
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity =( orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity =( orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('cart was updated', safe=False)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        
    else:
        print("user is not logged in")
        customer, order = guestOrder(request, data)

    total = float(data['userFormData']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shippingInfo']['address'],
            city = data['shippingInfo']['city'],
            state = data['shippingInfo']['state'],
            zipcode = data['shippingInfo']['zipcode'],
        )


    return JsonResponse('payment completed!!!', safe=False)