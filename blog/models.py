from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse # Redirect to the detail view of the post after creation or update

class Post(models.Model):
    title = models.CharField(max_length=100) # Title of the post
    content = models.TextField() # Content of the post
    created_at = models.DateTimeField(default=timezone.now) # Creation date of the post
    author = models.ForeignKey(User, on_delete=models.CASCADE) # If the user is deleted, their posts will also be removed

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Redirect to the detail view of the post after creation or update."""
        # 'post-detail' is the name of the URL pattern for the post detail view        
        return reverse('post-detail', kwargs={'pk': self.pk})
    