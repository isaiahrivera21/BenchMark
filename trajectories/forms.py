from django import forms
from .models import Trajectory

class TrajectoryForm(forms.ModelForm):
    # Add a new field for the single value when objective is SAME
    same_value = forms.IntegerField(required=False)

    class Meta:
        model = Trajectory
        exclude = ['timestamps', 'projected_points', 'actual_points']

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
            elif goal_type == Trajectory.EXERCISE:
                self.fields['focus_area'].widget = forms.TextInput()

        # Initialize objective-based fields
        if self.instance.pk:
            if self.instance.objective == Trajectory.SAME:
                self.fields['same_value'].initial = self.instance.current_amount
                self.fields['current_amount'].widget = forms.HiddenInput()
                self.fields['future_amount'].widget = forms.HiddenInput()
            else:
                self.fields['same_value'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        goal_type = cleaned_data.get('goal_type')
        objective = cleaned_data.get('objective')
        current_amount = cleaned_data.get('current_amount')
        future_amount = cleaned_data.get('future_amount')
        same_value = cleaned_data.get('same_value')
        
        if goal_type == Trajectory.FOOD:
            focus_area = cleaned_data.get('focus_area')
            valid_choices = [choice[0] for choice in Trajectory.FOOD_FOCUS_CHOICES]
            if focus_area not in valid_choices:
                self.add_error('focus_area', f'Invalid focus area for food goal. Must be one of: {", ".join(valid_choices)}')

        # Validate objective conditions
        if objective == Trajectory.INCREASE and future_amount <= current_amount:
            self.add_error('future_amount', 'For "INCREASE" objective, future_amount must be greater than current_amount.')
        elif objective == Trajectory.DECREASE and future_amount >= current_amount:
            self.add_error('future_amount', 'For "DECREASE" objective, future_amount must be less than current_amount.')
        elif objective == Trajectory.SAME:
            if same_value is None:
                self.add_error('same_value', 'This field is required for "SAME" objective.')
            else:
                cleaned_data['current_amount'] = same_value
                cleaned_data['future_amount'] = same_value

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.objective == Trajectory.SAME:
            instance.current_amount = instance.future_amount = self.cleaned_data.get('same_value')
        if commit:
            instance.save()
        return instance