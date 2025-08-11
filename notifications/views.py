from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})
