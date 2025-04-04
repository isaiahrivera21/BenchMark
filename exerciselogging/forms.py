from django import forms
from .models import UserLoggedExercise

class UserLoggedExerciseForm(forms.ModelForm):
    class Meta:
        model = UserLoggedExercise
        exclude = ['user']