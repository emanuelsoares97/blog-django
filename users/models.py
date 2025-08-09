from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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
        super().save(*args, **kwargs)  # Call the original save method

        img = Image.open(self.image.path) # Open the image file

        # Resize the image if it exceeds 300x300 pixels
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

