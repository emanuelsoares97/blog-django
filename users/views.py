from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, CustomLoginForm

from allauth.socialaccount.providers import registry
from allauth.account.views import LoginView
from blog.models import Post

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from django.core.paginator import Paginator

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomLoginForm  # Use your custom login form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  get_class_list() providers socials
        context['socialaccount_providers'] = registry.get_class_list()
        return context
        


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created {username}!')
            
            form.save() 

            return redirect('login')
        else:
            messages.error(request, 'Error creating account. Please try again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, 
                                instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating profile. Please try again.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts
    }
    return render(request, 'users/profile.html', context)



def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    if request.user.is_authenticated and request.user == profile_user:
        return redirect('profile')

    posts_qs = Post.objects.filter(author=profile_user).order_by('-created_at')

    paginator = Paginator(posts_qs, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'users/public_profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_paginated': posts.has_other_pages(),
        'page_obj': posts
    })
