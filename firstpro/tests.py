from ast import arg
from email.mime import image
import imp
from sys import implementation
from turtle import home, title
from venv import create
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from customer.views import *
from cart.views import *
from products.views import *
from checkout.views import *
from notification.views import *
from owner.views import *
from pages.views import *
from cart.models import *
from notification.models import *
from checkout.models import *
from customer.models import *
from products.models import *
from django.contrib.auth.models import Group
import datetime


class TestUrls(SimpleTestCase):
    
    def test_login_view(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_view)

    def test_registration_view(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, registration_view)

    def test_update_customer(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, homepage_view)

    def test_contact(self):
        url = reverse('contact')
        self.assertEquals(resolve(url).func, contact)

    def test_productbycategory(self):
        url = reverse('product-by-category', args=[1])
        self.assertEquals(resolve(url).func, product_category_view)

    def test_product(self):
        url = reverse('product', args=[1])
        self.assertEquals(resolve(url).func, product_view)

    def test_owner(self):
        url = reverse('owner')
        self.assertEquals(resolve(url).func,  admin_view)

    def test_owner_orders(self):
        url = reverse('owner-orders')
        self.assertEquals(resolve(url).func, admin_order_view)

    def test_delete_orders(self):
        url = reverse('delete-orders', args=[1])
        self.assertEquals(resolve(url).func,  delete_shipping_order)

    def test_manage_customer(self):
        url = reverse('manage-customer')
        self.assertEquals(resolve(url).func, manageCustomer)

    def test_update_customers(self):
        
        url = reverse('update-customer', args=[1])
        self.assertEquals(resolve(url).func, updateCustomer)

    def test_delete_customers(self):
        url = reverse('delete-customer', args=[1])
        self.assertEquals(resolve(url).func, deleteCustomer)

    def test_manage_product(self):
        url = reverse('manage-product')
        self.assertEquals(resolve(url).func, manageProduct)

    def test_update_product(self):
        
        url = reverse('update-product', args=[1])
        self.assertEquals(resolve(url).func, updateProduct)

    def test_delete_product(self):
        
        url = reverse('delete-product', args=[1])
        self.assertEquals(resolve(url).func, deleteProduct)

    def test_checkout(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout_view)

    def test_update_cart(self):
        url = reverse('update-cart')
        self.assertEquals(resolve(url).func, update_data_view)

    def test_proceses_checkout(self):
        url = reverse('process-checkout')
        self.assertEquals(resolve(url).func, processCheckout)

    def test_search(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, searchProducts)

    def test_create_product(self):
        url = reverse('create-product')
        self.assertEquals(resolve(url).func, create_products_view)

    def test_logout(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)

    def test_update_discount(self):
        url = reverse('update-discount')
        self.assertEquals(resolve(url).func,  update_discount_view)

    def test_rootpage(self):
        url = reverse('rootpage')
        self.assertEquals(resolve(url).func,  rootpage)

    def test_user_profile(self):
        url = reverse('user-profile')
        self.assertEquals(resolve(url).func, user_profile_view)

    def test_delete_account(self):
        url = reverse('delete-account', args=[1])
        self.assertEquals(resolve(url).func, delete_account)

    def test_change_password(self):
        url = reverse('change-password',args= [1])
        self.assertEquals(resolve(url).func, changePassword)

class test_views(TestCase):
    def test_customer_dashboard(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()

        url = reverse('manage-customer')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'owner/manage_customer.html')

    def test_update_customer(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            id =1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        url = reverse('update-customer', args=[customer.id])
        response = client.post(url, {
            'user': user,
            'name' : 'new full name',
            'email':'test@email.com',
            'phone' :'918181818',
            'username' :'username',
            'password': 'password'

        })
        
        customer.refresh_from_db()
    

        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(customer.name, 'new full name')
        self.assertRedirects(response, '/manage-customer/')

    
    
    def test_delete_customer(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        customer.refresh_from_db()

        url = reverse('delete-customer', args=[customer.id])
        response = client.post(url)
        print(response.status_code)

        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()
      
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/manage-customer/')

    def test_register(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        loggged_in = client.login(username="username", password="password")
        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()
        url = reverse('register')
        response = client.post(url, {
            'name': 'first name',
            'email': 'test email',
            'address': 'test adr',
            'phone': 'phone',
            'username': 'username22',
            'password': 'password'
        })

        print(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "registration.html")

    def test_product_dashboard(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()
      
        url = reverse('manage-product')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'owner/manageProduct.html')

    def test_update_product(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")
        
        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()

        product = Product.objects.create(
            title='product title',
            description ='product description',
            price = 100
        )

        cat = Category.objects.create(name='new')
        cat_id = cat.id

        url = reverse('update-product', args=[product.id])
        response = client.post(url, {
            'title':'new product title',
            'description': 'new product description',
            'price': 1200,
            'category': cat_id

        })
        
        product.refresh_from_db()
    

        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(product.title, 'new product title')
        self.assertRedirects(response, '/manage-product/')

    
    
    def test_delete_product(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")
    
        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()

        product = Product.objects.create(
            id=1,
            title='product title',
            description = 'desc',
            vote_total =1 ,
            vote_ratio = 1,
            price = 100,
            stock_quantity = 10,
            in_stock = True
        )

        url = reverse('delete-product', args=[product.id])
        response = client.post(url)
      
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/manage-product/')
    
    def test_adminCheckout(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()

        url = reverse('owner-orders')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'owner/admin_orders.html')

    def test_addOrder(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        
        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        product = Product.objects.create(
            title='product title',
            description ='product description',
            price = 100
        )

        url = reverse('create-order')
        response = client.post(url, {
             'customer':customer.id,
             'item': product.id,
             'status': 'Pending',
             'quantity': 5,
             'address':'test address',
             'city': 'test city',
             


        })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/owner-orders/')
    
    def test_updateOrder(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        
        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        product = Product.objects.create(
            title='product title',
            description ='product description',
            price = 100
        )
        order = Order.objects.create(customer=customer, status='Pending', order_id=datetime.datetime.now().timestamp(), order_completed=False)
        order.save()
        orderproduct = OrderProduct.objects.create(order=order,
        item=product, quantity = 10)
        orderproduct.save()
        shipping = Shipping.objects.create(customer=customer,
        order=order, city='test city', address= 'test address')
        shipping.save()
        url = reverse('update-order', args=[orderproduct.id])
        response = client.post(url, {
             'customer':customer.id,
             'item': product.id,
             'status': 'In Process',
             'quantity': 5,
             'address':'updated address',
             'city': 'updated city',
            
        })
        order.refresh_from_db()
        orderproduct.refresh_from_db()
        shipping.refresh_from_db()
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(shipping.address, 'updated address')
        self.assertEquals(orderproduct.quantity, 5)
        self.assertRedirects(response, '/owner-orders/')

    def test_del_shipping_order(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        product = Product.objects.create(
            title='product title',
            description ='product description',
            price = 100
        )
        order, created = Order.objects.get_or_create(
            customer=customer, order_completed=False, order_id=datetime.datetime.now().timestamp())
        order.save()
        orderProduct = OrderProduct.objects.create(
             item=product, order=order, quantity=5)

      

        url = reverse('delete-orders', args=[orderProduct.id])
        response = client.post(url)
        print(response.status_code)
      
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/owner-orders/')

    def test_product_detail(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        
        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        
        product = Product.objects.create(
            title='product title',
            description ='product description',
            price = 100
        )
        url = reverse('product', args=[product.id])
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/detail.html')
    
    def test_notification_view(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        
        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        notification = Notification.objects.create(
            id = '6db5175c-d5cd-4e9c-a054-54e3d54474ec',
            title='Testing notification',
            description = 'testing the notification feature'
        )
        url = reverse('notifications')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
    
    def test_notification_delete(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        
        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        notification = Notification.objects.create(
            id = '6db5175c-d5cd-4e9c-a054-54e3d54474ec',
            title='Testing notification',
            description = 'testing the notification feature'
        )
        url = reverse('delete', args=[notification.id])    
        response = client.post(url)

        self.assertEquals(response.status_code, 302)    

    # admin part test 
    def test_search(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()
      
        url = reverse('search')
        response = client.get(url, {
            'search': 'dog'
        }
    
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
    
    def order_history(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()
      
        url = reverse('orderhistory', args=[customer.id])
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'orderhistory.html')
    
    def update_cart(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()
       
        product = Product.objects.create(
            title='product title',
            description ='product description',
            price = 100
        )
        order = Order.objects.create(
            customer=customer)
        order.save()
        orderProduct = OrderProduct.objects.create(
             item=product, order=order, quantity=5)
        items = order.orderproduct_set.all()
        cartItems = order.getCartItems
      
        url = reverse('update-cart')
        response = client.get(url, {
            'productId': product.id,
            'action': "add"
        })

        self.assertEquals(response.status_code, 200)
        

    
    def review_cart(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        group = Group.objects.create(name='admin')
        user.groups.add(group)
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            id=1,
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        customer.refresh_from_db()
       
        product = Product.objects.create(
            title='product title',
            description ='product description',
            price = 100
        )
        order = Order.objects.create(
            customer=customer)
        order.save()
        orderProduct = OrderProduct.objects.create(
             item=product, order=order, quantity=5)
        items = order.orderproduct_set.all()
        cartItems = order.getCartItems
      
        url = reverse('checkout')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')