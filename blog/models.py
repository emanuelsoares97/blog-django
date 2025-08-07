from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse # Redirect to the detail view of the post after creation or update

class Post(models.Model):
    title = models.CharField(max_length=100) # Title of the post
    content = models.TextField() # Content of the post
    created_at = models.DateTimeField(default=timezone.now) # Creation date of the post
    author = models.ForeignKey(User, on_delete=models.CASCADE) # If the user is deleted, their posts will also be removed
    updated_at = models.DateTimeField(auto_now=True) # Automatically update the timestamp when the post is modified


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Redirect to the detail view of the post after creation or update."""
        # 'post-detail' is the name of the URL pattern for the post detail view        
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # Link comment to a post
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Author of the comment
    content = models.TextField() # Content of the comment
    created_at = models.DateTimeField(default=timezone.now) # Creation date of the comment
    approved = models.BooleanField(default=False) # Whether the comment is approved for display
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE) # For threaded comments

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'
    
    def approved_comments(self):
        """Return approved comments."""
        return self.comments.filter(approved=True)
    
    