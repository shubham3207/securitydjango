"""firstpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import thep include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from unicodedata import name
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from pages.views import *

from products.views import *

from customer.views import *
from owner.views import *

from cart.views import *

from checkout.views import *

from notification.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),

    path('register/', registration_view, name='register'),
    # path('activate/<uidb46>/<token>', activate, name='activate'),
    path('', homepage_view, name='home'),
    path('contact/', contact, name='contact'),
    path('product/<int:id>/', product_view, name='product'),
    path('product-by-category/<str:choice>/',
         product_category_view, name='product-by-category'),
     path('product-by-subcategory/<str:subcategory>/',
         product_sub_category_view, name='product-by-subcategory'),
    path('cart/', cart_view, name='cart'),

    path('owner/', admin_view, name='owner'),
    path('owner-orders/', admin_order_view, name='owner-orders'),
    path('owner/delete-orders/<int:pk>',
         delete_shipping_order, name='delete-orders'),
    path('manage-customer/', manageCustomer, name='manage-customer'),
    path('update-customer/<int:pk>/', updateCustomer, name='update-customer'),
    path('delete-customer/<int:pk>/', deleteCustomer, name='delete-customer'),
    path('manage-product/', manageProduct, name='manage-product'),
    path('update-product/<int:pk>/', updateProduct, name='update-product'),
    path('delete-product/<int:pk>/', deleteProduct, name='delete-product'),
    path('create-order', createOrder,  name='create-order'),
    path('update-order/<int:pk>/', updateOrder, name='update-order'),

    path('checkout/', checkout_view, name='checkout'),
    path('update-cart/', update_data_view, name='update-cart'),
    path('process-checkout/', processCheckout, name='process-checkout'),
    path('search/', searchProducts, name='search'),

    path('create-product', create_products_view, name='create-product'),



    path('logout/', logoutUser, name='logout'),
    path('update-discount/', update_discount_view, name='update-discount'),
    path('root/', rootpage, name="rootpage"),
    path('contact/', contact, name="contact"),
    path('aboutus/', aboutus, name='aboutus' ),
     path('helppage/', helppage, name='helppage' ),
    path('user-profile/', user_profile_view, name='user-profile'),
    path('delete-account/<int:pk>/', delete_account, name='delete-account'),
  
    path('change-password/<int:pk>/', changePassword, name='change-password'),
    path('update-account/<int:pk>/', update_account, name='update-account'),
    path('baseuser', baseuser),

    path('grooming/', grooming, name='grooming'),
    path('pethostel/', pethostel, name='pet-hostel'),
    path('vaccine/', vaccine, name='vaccination'),

    path('notifications/', notification_view, name='notifications'),
    path('delete/<str:pk>/', notification_delete, name='delete'),

    path('create-message', message_view, name='create-message'),
    path('manage-messages/', manageMessages, name='manage-message'),
    path('delete-message/<int:pk>/', deleteMessage, name='delete-message'),

    path('orderhistory/<int:pk>/', order_history, name='orderhistory'),

]

# appending to the list
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
