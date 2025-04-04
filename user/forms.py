from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    height = forms.FloatField(required=False)
    weight = forms.FloatField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'height', 'weight')
