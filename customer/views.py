from email import message
from urllib import request
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
from django.contrib import messages

def user_profile_view(request):
    return render(request, 'customer/userprofile.html')

def delete_account(request,pk):
    customer = Customer.objects.get(id=pk)
    customer.delete()
    logout(request)
    messages.success(request, "Your acccount has been deleted")
    return redirect("/")

def deleteAccount(request, pk):
    customer = Customer.objects.get(id=pk)
    print(customer)
    if request.method == 'POST':
        password = request.POST.get('password')
        print(password)
        if password == customer.password:
            customer.user.delete()
            return redirect('/')
    return render(request, 'customer/deleteAccount.html')


def baseuser(request):
    return render(request, 'customer/base-user.html')

def changePassword(request, pk):
    customer = Customer.objects.get(id=pk)
    user = request.user
    print(customer)
    if request.method == 'POST':
        password = request.POST.get('old-password')
        new_password = request.POST.get('new-password')
        confirm_passowrd = request.POST.get('confirm-password')
        if password == customer.password:
            if new_password == confirm_passowrd:
                customer.password = new_password
                customer.save()
                user.set_password(new_password)
                user.save()

        print(password)
        

    return render(request, 'customer/changePassword.html')


def update_account(request, pk):
    customer = Customer.objects.get(id=pk)
    user = request.user
    form = CustomerForm(request.POST)
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        username = request.POST.get('username')
        if username != customer.username:
                user.username = username
                user.save()
                customer.username = username
        customer.save()
        return redirect('/user-profile/')
    context = {'form': form, 'customer': customer}
    return render(request, 'customer/updateAccount.html', context)

def order_history(request, pk):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=pk)
        user = request.user
        order = Order.objects.filter(customer=customer)
    else:
        order = []
    context = {'order_history':order}

    return render(request, 'orderhistory.html', context)