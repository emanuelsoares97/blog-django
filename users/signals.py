from django.db.models.signals import post_save #
from django.contrib.auth.models import User
from django.dispatch import receiver 
from .models import Profile
import requests
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    """Signal to create a Profile instance when a User is created."""

    if created:
        Profile.objects.create(user=instance) # Create a Profile for the new User

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Signal to save the Profile instance when the User is saved.
    This ensures that the Profile is always up-to-date with the User's information."""
    
    instance.profile.save()  # Save the Profile associated with the User



import requests
from allauth.account.signals import user_logged_in
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def save_profile_picture_on_login(request, user, **kwargs):
    """
    Signal to save the user's profile picture from Google on login.
    Works with CloudinaryField and avoids overwriting existing images
    unless they are not from Google.
    """
    try:
        social_account = user.socialaccount_set.filter(provider='google').first()
        if not social_account:
            return

        picture_url = social_account.extra_data.get('picture')
        if not picture_url:
            return

        profile = getattr(user, 'profile', None)
        if not profile:
            return

        # Only save if no image exists or current image is not from Google
        current_image_name = getattr(profile.image, 'name', '')
        if not profile.image or 'google' not in current_image_name.lower():
            response = requests.get(picture_url)
            response.raise_for_status()
            file_name = f"{user.username}_google.jpg"
            profile.image.save(file_name, ContentFile(response.content), save=True)

    except Exception as e:
        logger.error(f"Error saving Google profile picture on login: {e}")
