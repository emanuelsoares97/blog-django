from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    bio = models.TextField(blank=True, null=True) 
    image = CloudinaryField(
        "image",
        folder="profile_pictures",
        blank=True, 
        null=True
    )
    location = models.CharField(max_length=100, blank=True, null=True) 
    birth_date = models.DateField(blank=True, null=True) 

    def __str__(self):
        return f"{self.user.username}'s Profile"  # String representation of the Profile model

    @property
    def image_url(self):
        """
        Return a secure (https) URL for the profile image if it exists,
        otherwise return the secure default image on Cloudinary.
        """
        url = getattr(self.image, "url", None) if self.image else None
        if not url:
            url = "https://res.cloudinary.com/dogevu6ip/image/upload/v1755528094/default_v7ayus.jpg"
        if url.startswith("http://"):
            url = url.replace("http://", "https://", 1)
        return url


