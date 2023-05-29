from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, response
from django.contrib import auth
from django.contrib.auth.models import User
from checkout.models import Shipping
# Create your views here.
from products.models import Product, Category
from customer.models import *
from customer.forms import CustomerForm, CreateUserForm
from cart.models import *
import json
from django.contrib.auth import authenticate, login, logout
import datetime
def checkout_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer.name)
        # get or create order
        order, created = Order.objects.get_or_create(
            customer=customer, order_completed=False)
        items = order.orderproduct_set.all()
        cartItems = order.getCartItems
    else:
        items = []
        order = {'getCartTotal': 0, 'getCartItems': 0}
        cartItems = order['getCartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping':False}
    return render(request, 'checkout.html', context)



def processCheckout(request):
    print(request.body)
    transactionId = datetime.datetime.now().timestamp()
    checkoutData = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, order_completed=False)
        cart_total= float(checkoutData['form']['cart_total'])
        order.order_id = transactionId
       

        if cart_total == order.getCartTotal:
            order.order_completed = True
        order.save()
        customer.reward_point = (customer.reward_point) + 0.5
        customer.save()
        

        if order.shipping == True:
            Shipping.objects.create(
                customer= customer,
                order = order,
                city = checkoutData['shipping']['city'],
                address = checkoutData['shipping']['address'],
            )
    else:
        print('no user')
    return JsonResponse('Order placed', safe=False)