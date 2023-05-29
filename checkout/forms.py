import imp
from django.forms import ModelForm
from .models import *


class ShippingForm(ModelForm):
    class Meta:
        model = Shipping    
        fields = '__all__'


