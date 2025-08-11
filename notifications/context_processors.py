from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        notifs = Notification.objects.filter(recipient=request.user, unread=True).order_by('-timestamp')[:5]
        count = Notification.objects.filter(recipient=request.user, unread=True).count()
        return {
            'unread_notifications_count': count,
            'latest_notifications': notifs
        }
    return {'unread_notifications_count': 0, 'latest_notifications': []}

