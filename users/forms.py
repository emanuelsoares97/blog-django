from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.') # Custom field for email

    class Meta:
        # Specify the model and fields to include in the form
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # what fields to include in the form

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.') # Custom field for email

    class Meta:
        # Specify the model and fields to include in the form
        model = User
        fields = ['username', 'email'] # what fields to include in the form

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        # Specify the model and fields to include in the form
        model = Profile
        fields = ['image']  # what fields to include in the form for Profile

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs.pop('aria-describedby', None)  