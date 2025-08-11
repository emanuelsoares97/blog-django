from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Notification(models.Model):
    """Model representing a notification."""
    NOTIFICATION_TYPES = (
        (1, 'like'),
        (2, 'comment'),
    )
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('blog.Comment', on_delete=models.CASCADE, null=True, blank=True)
    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification to {self.recipient} from {self.sender}'

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.post.id)]) if self.post else '#'
