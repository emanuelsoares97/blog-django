from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), # Home page with list of posts
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # Detail view for a specific post
    path('post/new/', PostCreateView.as_view(), name='post-create'), # Create a new post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # Edit a post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # Delete a post
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'), # List posts by a specific user
]