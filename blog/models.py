from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100) # título do post
    content = models.TextField() # conteúdo do post
    created_at = models.DateTimeField(default=timezone.now)    # data de criação do post
    author = models.ForeignKey(User, on_delete=models.CASCADE) #se o user for eliminado, os posts dele também serão removidos

    def __str__(self):
        return self.title