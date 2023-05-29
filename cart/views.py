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
from django. contrib import messages
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
def cart_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, order_completed=False)
        items = order.orderproduct_set.all()
    else:
        items = []
        order = {'getCartTotal': 0, 'getCartItems': 0,'shipping':False}
        

    context = {'items': items, 'order': order}
    return render(request, "cart.html", context)

def update_data_view(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(action, productId)

    customer = request.user.customer
    item = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, order_completed=False)
    orderProduct, created = OrderProduct.objects.get_or_create(
        order=order, item=item)

    if action == 'add':
        
        orderProduct.quantity = (orderProduct.quantity + 1)
        item.buy_count = (item.buy_count + 1)
        if item.stock_quantity is not None:
            item.stock_quantity = (item.stock_quantity-1)
        
        
    elif action == 'remove':
        orderProduct.quantity = (orderProduct.quantity - 1)  
        item.buy_count = (item.buy_count + 1)
        if item.stock_quantity is not None:
            if item.stock_quantity > 0:
                item.stock_quantity = (item.stock_quantity+1)
        
    
    
    orderProduct.save()
    item.save()
   
    

    if orderProduct.quantity <= 0:
        orderProduct.delete()

    return JsonResponse('Item added to cart', safe=False)

