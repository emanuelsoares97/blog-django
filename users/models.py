from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link to the User model
    bio = models.TextField(blank=True, null=True) # Optional biography field
    image = models.ImageField(default='default.jpg', upload_to='profile_pictures/', blank=True, null=True) # Optional profile picture field
    location = models.CharField(max_length=100, blank=True, null=True) # Optional location field
    birth_date = models.DateField(blank=True, null=True) # Optional birth date field

    def __str__(self):
        return f"{self.user.username}'s Profile"  # String representation of the Profile model
