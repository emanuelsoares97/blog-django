from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from blog.models import Post, Comment
from .models import Notification



@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    
    if created and instance.post.author != instance.author:
        Notification.objects.create(
            recipient=instance.post.author,  #owner post
            sender=instance.author,         # who commented
            notification_type=2,           # 2 = comment
            post=instance.post,
            comment=instance
        )



@receiver(m2m_changed, sender=Post.likes.through)
def create_like_notification(sender, instance, action, pk_set, **kwargs):

    if action == 'post_add':
        for user_id in pk_set:
            if instance.author.id != user_id:
                Notification.objects.create(
                    recipient=instance.author, #owner post
                    sender_id=user_id,     # who liked
                    notification_type=1,     # 1 = like
                    post=instance
                )
