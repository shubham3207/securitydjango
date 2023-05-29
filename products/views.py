from unicodedata import name
from django.shortcuts import render
from .forms import ProductForm, ReviewForm
from .models import Product, Category
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
from django.contrib import messages
import json
from django.contrib.auth import authenticate, login, logout
import datetime
# Create your views here.
def create_products_view(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    object = Category.objects.all()
    subCat = NewSubCategory.objects.all()
    context = {'form': form, 'object': object, 'subcategory': subCat}
    return render(request, 'product/createproduct.html', context)

def product_view(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
    # get or create order
        order, created = Order.objects.get_or_create(
            customer=customer, order_completed=False)
        items = order.orderproduct_set.all()
        cartItems = order.getCartItems
    else:
        items = []
        order = {'getCartTotal': 0, 'getCartItems': 0}
        cartItems = order['getCartItems']
    object = Product.objects.get(id=id)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.product = object
        review.owner = request.user.customer
        review.save()

        #update rate count
        object.getVoteCount

        messages.success(request, 'Your review was successfully submitted')
        return redirect('product' , id=object.id)

    context = {'object': object, 'cartItems': cartItems,'shipping':False, 'form':form}
    return render(request, "product/detail.html", context)

def product_category_view(request, choice):
    category_object = Category.objects.get(name=(choice or choice.parent_category.name))
    category_id = category_object.id
    
    sort_by = request.GET.get("sort", "low-to-high")
    if sort_by == "low-to-high":
        products = Product.objects.filter(category = category_id).order_by("price")
    elif sort_by == "high-to-low":
        products = Product.objects.filter(category = category_id).order_by("-price")
    elif sort_by == "popularity":
        products = Product.objects.filter(category = category_id).order_by("buy_count")
    else:
        products = Product.objects.filter(category = category_id)


    context = {'products': products}

    return render(request, "product/category.html", context)

def product_sub_category_view(request, subcategory):
    subcategory_object = NewSubCategory.objects.get(name=subcategory)
    subcategory_id = subcategory_object.id
    
    sort_by = request.GET.get("sort", "low-to-high")
    if sort_by == "low-to-high":
        products = Product.objects.filter(subcategory = subcategory_id).order_by("price")
    elif sort_by == "high-to-low":
        products = Product.objects.filter(subcategory = subcategory_id).order_by("-price")
    elif sort_by == "popularity":
        products = Product.objects.filter(subcategory = subcategory_id).order_by("buy_count")
    else:
        products = Product.objects.filter(subcategory = subcategory_id)


    context = {'products': products}

    return render(request, "product/category.html", context)