import imp
from django.forms import ModelForm
from .models import *


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class OrderProductForm(ModelForm):
    class Meta:
        model = OrderProduct
        fields = '__all__'

