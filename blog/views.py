from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import CommentForm
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 5
    ordering = ["-created_at"]

    def get_queryset(self):
        # prefetch de comments só com campos essenciais (opcional)
        comments_qs = Comment.objects.only("id", "post_id")
        return (
            Post.objects
            .select_related("author", "author__profile")   
            .prefetch_related(
                "likes",  
                Prefetch("comments", queryset=comments_qs), 
            )
            .annotate(
                likes_count=Count("likes", distinct=True),
                comments_count=Count("comments", distinct=True),
            )
            .order_by("-created_at")
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'post'  # Name of the variable to access in the template

    def get_context_data(self, **kwargs):
        """Add the comment form to the context."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['parent_comments'] = self.object.comments.filter(parent_comment__isnull=True).order_by('-created_at')
        context['replies'] = self.object.comments.filter(parent_comment__isnull=False)


        return context

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new post.
    Only logged-in users can create posts."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['content']

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
    fields = ['content']

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


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # Create a comment instance but don't save it yet
            comment.post = post # Link the comment to the post
            comment.author = request.user # Set the author of the comment to the current user

            parent_id = request.POST.get('parent_comment')
            if parent_id:
                
                comment.parent_comment = Comment.objects.get(pk=parent_id) # Set the parent comment if it exists
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm() # Create an empty form

    return redirect(post.get_absolute_url()) # Redirect to the post detail view after adding the comment

@login_required
@require_POST
def toggle_like_post_ajax(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    data = {
        'liked': liked,
        'total_likes': post.likes.count(),
    }
    return JsonResponse(data)