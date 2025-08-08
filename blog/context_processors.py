from django.db.models import Count
from django.contrib.auth.models import User
from .models import Post

def sidebar_data(request):
    # Post com mais likes
    post_max_likes = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes').first()

    # Post com mais comentários
    post_max_comments = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments').first()

    # Usuário com mais posts
    user_max_posts = User.objects.annotate(num_posts=Count('post')).order_by('-num_posts').first()

    return {
        'post_max_likes': post_max_likes,
        'post_max_comments': post_max_comments,
        'user_max_posts': user_max_posts,
    }
