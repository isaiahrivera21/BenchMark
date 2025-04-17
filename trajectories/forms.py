from django import forms
from .models import Trajectory

class TrajectoryForm(forms.ModelForm):
    class Meta:
        model = Trajectory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize with text input
        self.fields['focus_area'].widget = forms.TextInput()
        
        # Update widget based on goal type
        if self.instance.pk or 'goal_type' in self.data:
            goal_type = self.data.get('goal_type') or self.instance.goal_type
            
            if goal_type == Trajectory.FOOD:
                self.fields['focus_area'].widget = forms.Select(
                    choices=[('', '---')] + Trajectory.FOOD_FOCUS_CHOICES
                )

    def clean(self):
        cleaned_data = super().clean()
        goal_type = cleaned_data.get('goal_type')
        
        if goal_type == Trajectory.FOOD:
            focus_area = cleaned_data.get('focus_area')
            valid_choices = [choice[0] for choice in Trajectory.FOOD_FOCUS_CHOICES]
            if focus_area not in valid_choices:
                self.add_error('focus_area', f'Invalid focus area for food goal. Must be one of: {", ".join(valid_choices)}')

        return cleaned_data