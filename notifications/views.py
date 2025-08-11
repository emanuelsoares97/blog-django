from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification
 

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})

@login_required
def notifications_list(request):

    # Get all notifications for the logged-in user
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    
    # Mark all notifications as read when the user views the list
    Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)

    return render(request, 'notifications/notifications_list.html', {
        'notifications': notifications
    })

