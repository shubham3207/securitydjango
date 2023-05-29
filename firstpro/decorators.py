from django.http import HttpResponse
from django.shortcuts import redirect

def user_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
           return redirect('home')
        else:
           return view_func(request, *args, **kwargs)

    return wrapper_func

def admin_restricted(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group == 'admin':
                return view_func(request, *args, **kwargs)
            if group == 'customer':
                return HttpResponse('You are a customer')
            else:
                return HttpResponse('You are not authorized')
        return wrapper_func
