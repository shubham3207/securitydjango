from email import message
from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
  


 