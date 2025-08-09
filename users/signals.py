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
    """Signal to save the Profile instance when the User is saved.
    This ensures that the Profile is always up-to-date with the User's information."""
    
    instance.profile.save()  # Save the Profile associated with the User



from allauth.account.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def save_profile_picture_on_login(request, user, **kwargs):
    """Signal to save the user's profile picture from Google on login."""
    try:
        social_account = user.socialaccount_set.filter(provider='google').first()
        if social_account:
            picture_url = social_account.extra_data.get('picture')
            if picture_url:
                profile = user.profile
                if not profile.image or 'google' not in profile.image.name:
                    import requests
                    from django.core.files.base import ContentFile

                    response = requests.get(picture_url)
                    response.raise_for_status()
                    file_name = f"{user.username}_google.jpg"
                    profile.image.save(file_name, ContentFile(response.content), save=True)
    except Exception as e:
        print("Erro ao salvar foto do Google no login:", e)
