from django.db.models.signals import post_save #
from django.contrib.auth.models import User
from django.dispatch import receiver 
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    """Signal to create a Profile instance when a User is created."""

    if created:
        Profile.objects.create(user=instance) # Create a Profile for the new User

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Signal to save the Profile instance when the User is saved."""
    
    instance.profile.save()  # Save the Profile associated with the User