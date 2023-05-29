from django.db import models
from cart.models import Order
from customer.models import Customer
from django.contrib import admin
# Create your models here.

class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.address

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'city', 'address', 'date_added')
admin.site.register(Shipping, ShippingAdmin)



