from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse # Redirect to the detail view of the post after creation or update

class Post(models.Model):
    content = models.TextField() # Content of the post
    created_at = models.DateTimeField(default=timezone.now) # Creation date of the post
    author = models.ForeignKey(User, on_delete=models.CASCADE) # If the user is deleted, their posts will also be removed
    updated_at = models.DateTimeField(auto_now=True) # Automatically update the timestamp when the post is modified
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True) # Users who liked the post


    def __str__(self):
        
        return self.content
    
    def get_absolute_url(self):
        """Redirect to the detail view of the post after creation or update."""
        # 'post-detail' is the name of the URL pattern for the post detail view        
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def total_likes(self):
        """Return the total number of likes for the post."""
        return self.likes.count()
    

    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # Link comment to a post
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Author of the comment
    content = models.TextField() # Content of the comment
    created_at = models.DateTimeField(default=timezone.now) # Creation date of the comment
    parent_comment = models.ForeignKey('self',
                                        null=True, 
                                        blank=True, 
                                        related_name='replies', 
                                        on_delete=models.CASCADE) # For threaded comments

    def __str__(self):
        return f'Comment by {self.author} on {self.post.content}'
    
    
    