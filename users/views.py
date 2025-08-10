from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, CustomLoginForm

from allauth.socialaccount.providers import registry
from allauth.account.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # ou 'account/login.html', conforme seu template
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

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

