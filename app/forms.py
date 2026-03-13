from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'user_type']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # If you want login via email