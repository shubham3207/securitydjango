import email
from django.shortcuts import render
from contact.forms import ContactForm
from contact.models import *
# Create your views here.
def message_view(request):
    contact_form = ContactForm()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        
        if contact_form.is_valid():
            contact_form.save()
            
    
    context = {'contact_form': contact_form}
    return render(request, 'contactnew.html', context)