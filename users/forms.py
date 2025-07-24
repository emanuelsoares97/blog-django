from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.') # Custom field for email

    class Meta:
        # Specify the model and fields to include in the form
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # what fields to include in the form