from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Property,Review

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'user_type']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # If you want login via email

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "title", "description", "property_type", "listing_status",
            "price", "location", "city", "province",
            "bedrooms", "bathrooms",
            "floor_area", "lot_area",
            "parking_spaces", "image", "is_available"
        ]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'image', 'rating', 'comment']