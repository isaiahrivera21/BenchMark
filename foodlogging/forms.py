from django import forms
from .models import UserLoggedFood

class UserLoggedFoodForm(forms.ModelForm):
    class Meta:
        model = UserLoggedFood
        exclude = ['user']