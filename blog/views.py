from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts' # Name of the variable to access in the template
    ordering = ['-created_at']  # Order by created_at descending

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'post'  # Name of the variable to access in the template

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new post.
    Only logged-in users can create posts."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # Automatically set the author to the current user
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the user is allowed to create a post."""
        return self.request.user.is_authenticated
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing post.
    Only logged-in users can update their posts."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # Automatically set the author to the current user
        return super().form_valid(form)


    def test_func(self):
        """Check if the user is allowed to update the post."""
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a post.
    Only logged-in users can delete their posts."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'  # Redirect to home after deletion


    def test_func(self):
        """Check if the user is allowed to delete the post."""
        post = self.get_object()
        if self.request.user == post.author:
            """Only the author of the post can delete it."""
            return True
        return False
    


def about(request):
    """About page view."""
    return render(request, 'blog/about.html', {'title': 'About'})
