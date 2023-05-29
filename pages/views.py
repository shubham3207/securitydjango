import imp
from multiprocessing import context
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
from django.contrib.sessions.backends.db import SessionStore
import datetime
from django.contrib import messages
from firstpro.decorators import *
from django.contrib.auth.decorators import login_required
from pages.activity_logger import log_activity
from datetime import datetime, timedelta

def login_view(request):
    users = User.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                customer = Customer.objects.get(user=user)
                username = customer.username
            except Customer.DoesNotExist:
                username = 'Unknown'

            log_activity(user, f'Logged in as {username}')

            return redirect('/')

    context = {'users': users}
    return render(request, "login.html", context)

def logoutUser(request):
    username = 'Anonymous'

    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            username = customer.username
        except Customer.DoesNotExist:
            pass

    logout(request)

    log_activity(request.user, f'Logged out | Username: {username}')

    return redirect('login')

import re
from django.contrib.auth.password_validation import (
    validate_password,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError

def registration_view(request):
    customer_form = CustomerForm()
    is_registered = False  # Flag to track registration completion

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)

        if customer_form.is_valid():
            un = customer_form.cleaned_data['username']
            em = customer_form.cleaned_data['email']
            pw = customer_form.cleaned_data['password']
            cpw = request.POST.get('confirmpassword')

            if pw == cpw:
                # Check if the password contains personal information
                if contains_personal_info(un, pw):
                    error_message = "Passwords should not include personal information."
                    messages.error(request, error_message)
                else:
                    try:
                        validate_password(
                            password=pw,
                            user=User,
                            password_validators=[
                                CommonPasswordValidator(),  # Prevent common passwords
                                NumericPasswordValidator(),  # Require at least one digit
                            ],
                        )
                        if len(pw) < 8 or len(pw) > 12:
                            raise ValidationError('Password must be 8-12 characters long.')
                        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', pw):
                            raise ValidationError('Password must include uppercase and lowercase letters, numbers, and special characters.')
                    except ValidationError as e:
                        messages.error(request, ', '.join(e.messages))
                    else:
                        user = User.objects.create_user(un, em, pw)
                        user.save()
                        customer = customer_form.save(commit=False)
                        customer.user = user
                        customer.save()
                        is_registered = True  # Set registration completion flag
                        messages.success(request, 'Your account has been registered')

                        log_activity(user, f'Registered as {un}')
            else:
                messages.error(request, "Passwords does not match")

    context = {'customer_form': customer_form, 'is_registered': is_registered}
    return render(request, 'registration.html', context)


def contains_personal_info(username, password):
    # Perform personal information check, e.g., using regular expressions
    # You can customize this function based on your specific requirements
    personal_info_patterns = [
        r"\b" + re.escape(username) + r"\b",  # Check for username
        r"\b\d{4}-\d{2}-\d{2}\b",  # Check for date of birth in format YYYY-MM-DD
        r"\b\d{10}\b"  # Check for phone number with 10 digits
    ]

    for pattern in personal_info_patterns:
        if re.search(pattern, password, re.IGNORECASE):
            return True

    return False




@login_required(login_url='login')
@admin_restricted
def admin_view(request):
    return render(request, "owner/admin.html")

@login_required(login_url='login')
@admin_restricted
def admin_order_view(request):
    checkout = Shipping.objects.all()
    orders_customer = Order.objects.all()
    orders_products = OrderProduct.objects.all()
    context = {'checkout': checkout, 'orders_customer': orders_customer, 'orders_products': orders_products}
    return render(request, "owner/admin_orders.html", context)


def homepage_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        customer = request.user.customer
    # get or create order
        order, created = Order.objects.get_or_create(
            customer=customer, order_completed=False)
        items = order.orderproduct_set.all()
        cartItems = order.getCartItems
    else:
        items = []
        order = {'getCartTotal': 0, 'getCartItems': 0, 'shipping':False }
        cartItems = order['getCartItems']
    object = Category.objects.all()


    context = {'object': object,
            'items': items, 
            'cartItems': cartItems}
    return render(request, "homepage.html", context)




def searchProducts(request):
    search_query = request.GET.get('search')
    products = Product.objects.all()

    if search_query:
        products = products.filter(title__icontains=search_query)

    context = {'products': products}

    if search_query:
        log_search_activity(request.user, search_query)

    return render(request, 'search.html', context)

def log_search_activity(user, search_query):
    username = 'Anonymous'
    if user.is_authenticated:
        try:
            customer = Customer.objects.get(user=user)
            username = customer.username
        except Customer.DoesNotExist:
            pass

    log_activity(user, f'Searched for products: {search_query} | Username: {username}')

def log_activity(user, message):
    # Replace this with your actual code to log the activity
    with open('activity_log.txt', 'a') as file:
        file.write(message + '\n')

def update_discount_view(request):
    data = json.loads(request.body)
    orderId = data['orderId']
    action = data['action']
    order = Order.objects.get(id=orderId)
    customer = order.customer
    print(action, orderId)
    if action == 'add-discount' :
        if order.used_discount_points <3 and order.used_discount_points>=0:
             order.used_discount_points = (order.used_discount_points + 1)
             customer.reward_point = (customer.reward_point-1)

        
        
    elif action == 'remove-discount':
        if order.used_discount_points>0:
            order.used_discount_points = (order.used_discount_points - 1)
            customer.reward_point = (customer.reward_point+1)

       

    
    order.save()
    customer.save()

    return JsonResponse('Discount', safe=False)

def rootpage(request):
    category = Category.objects.all()

    context = {'category':category}
    return render(request, "rootpage.html", context)

def contact(request):
    return render(request, 'contactnew.html')

def grooming(request):
    return render(request, "services/grooming.html")

def pethostel(request):
    return render(request, "services/pethostel.html")

def vaccine(request):
    return render(request, "services/vaccine.html")

def aboutus(request):
    return render(request, 'aboutus.html')

def helppage(request):
    return render(request, 'helppage.html')

