from django.shortcuts import render, redirect
from notification.models import Notification
from django.contrib import messages

def notification_view(request):
    notifications = Notification.objects.all
    context = {'notice':notifications}
    return render(request, "notifications.html", context)

def notification_delete(request,pk):
    if request.user.is_superuser:
        notifications = Notification.objects.get(id=pk)

        if request.method == 'POST':
            notifications.delete()
            return redirect('home')
            
        context = {'object': notifications}
        return render(request, "delete_notification.html", context)
    else:
        messages.success(request, "You don't have permission")
        return redirect("/")

