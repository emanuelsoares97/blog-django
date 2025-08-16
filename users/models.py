from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os 
import logging

logger = logging.getLogger(__name__)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link to the User model
    bio = models.TextField(blank=True, null=True) 
    image = models.ImageField(default='default.jpg', upload_to='profile_pictures/', blank=True, null=True) 
    location = models.CharField(max_length=100, blank=True, null=True) 
    birth_date = models.DateField(blank=True, null=True) 

    def __str__(self):
        return f"{self.user.username}'s Profile"  # String representation of the Profile model

    def save(self, *args, **kwargs):
            """Override the save method to resize the profile image."""
            super().save(*args, **kwargs)

            if self.image and hasattr(self.image, 'path'):
                image_path = self.image.path
                if os.path.exists(image_path):
                    try:
                        img = Image.open(image_path)
                        # Resize the image if it exceeds 300x300 pixels
                        if img.height > 300 or img.width > 300:
                            output_size = (300, 300)
                            img.thumbnail(output_size)
                            img.save(image_path)
                    except Exception as e:
                        logger.error(f"Erro ao abrir/processar imagem do perfil: {e}")

