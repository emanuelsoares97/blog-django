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

import requests
from django.core.files.base import ContentFile
from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users.models import Profile

@receiver([social_account_added, social_account_updated])
def save_google_profile_picture(sender, request, sociallogin, **kwargs):
    print("Signal executado para usuário:", sociallogin.user)
    if sociallogin.account.provider == 'google':
        user = sociallogin.user
        profile, _ = Profile.objects.get_or_create(user=user)
        picture_url = sociallogin.account.extra_data.get('picture')
        print("URL da foto:", picture_url)
        if picture_url:
            try:
                response = requests.get(picture_url)
                response.raise_for_status()
                file_name = f"{user.username}_google.jpg"
                profile.image.save(file_name, ContentFile(response.content), save=True)
                print("Foto salva com sucesso!")
            except Exception as e:
                print("Erro ao copiar foto do Google:", e)

