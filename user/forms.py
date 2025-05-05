# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser
# from django.core.validators import MinValueValidator, MaxValueValidator

# class CustomUserCreationForm(UserCreationForm):
#     feet = forms.IntegerField(required=False,label='Feet',validators=[MinValueValidator(0)])
#     inches = forms.IntegerField(required=False,label='Inches',validators=[MinValueValidator(0), MaxValueValidator(11)])
#     weight = forms.FloatField(required=False)

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'password1', 'password2', 'feet', 'inches', 'weight')
#         exclude = ('height',)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Convert stored height to feet and inches for existing users
#         if self.instance.pk and self.instance.height is not None:
#             total_inches = self.instance.height * 12
#             self.initial['feet'] = int(total_inches // 12)
#             self.initial['inches'] = int(total_inches % 12)

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         # Calculate height from feet and inches
#         feet = self.cleaned_data.get('feet', 0)
#         inches = self.cleaned_data.get('inches', 0)
#         user.height = (feet*12.0 + (inches)) * 2.54 # converts to CM 
#         if commit:
#             user.save()
#         return user

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    feet = forms.IntegerField(required=False, label='Feet', validators=[MinValueValidator(0)])
    inches = forms.IntegerField(required=False, label='Inches', validators=[MinValueValidator(0), MaxValueValidator(11)])
    weight = forms.FloatField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'gender', 'activity_level', 'feet', 'inches', 'weight', 'age', 'pace_unit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.height is not None:
            total_inches = self.instance.height * 12
            self.initial['feet'] = int(total_inches // 12)
            self.initial['inches'] = int(total_inches % 12)

    def save(self, commit=True):
        user = super().save(commit=False)
        # Calculate height from feet and inches
        feet = self.cleaned_data.get('feet', 0)
        inches = self.cleaned_data.get('inches', 0)
        user.height = (feet * 12.0 + inches) * 2.54  # Convert to centimeters

        # Initialize weight log with current date and provided weight
        weight = self.cleaned_data.get('weight')
        if weight:
            if user.weight_log is None:
                user.weight_log = []
            if user.weight_log_dates is None:
                user.weight_log_dates = []
            user.weight_log.append(weight)
            user.weight_log_dates.append(timezone.now().date())

        if commit:
            user.save()
        return user