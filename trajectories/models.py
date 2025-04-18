from django.db import models
from django.core.exceptions import ValidationError
from user.models import CustomUser
from django.contrib.postgres.fields import ArrayField

class Trajectory(models.Model):
    # Existing choices
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    PACE_CHOICES = [
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
        (YEARLY, "Yearly"),
    ]

    INCREASE = "INCREASE"
    DECREASE = "DECREASE"
    SAME = "SAME"
    OBJECTIVE_CHOICES = [
        (INCREASE, "Increase"),
        (DECREASE, "Decrease"),
        (SAME, "Same"),
    ]

    # Goal type choices
    FOOD = 'FOOD'
    EXERCISE = 'EXERCISE'
    GOAL_TYPE_CHOICES = [
        (FOOD, 'Food'),
        (EXERCISE, 'Exercise'),
    ]

    # Focus area options for food goals
    FOOD_FOCUS_CHOICES = [
        ('CALORIES', 'Calories'),
        ('CARBS', 'Carbohydrates'),
        ('PROTEIN', 'Protein'),
        ('SODIUM', 'Sodium'),
        ('FAT','Fat'),
        ('CHOLESTOROL','Cholesterol')
    ]

    pace_type = models.CharField(max_length=50, choices=PACE_CHOICES)
    start_date = models.DateField(auto_now_add=True)
    target_date = models.DateField("Target Date")
    
    current_amount = models.IntegerField(null=False, blank=False)
    future_amount = models.IntegerField(null=False, blank=False)
    objective = models.CharField(max_length=50, choices=OBJECTIVE_CHOICES)
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPE_CHOICES)
    focus_area = models.TextField()  # Will be either dropdown choice or free text
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)

    # Arrays to contain the trajectory data
    timestamps = ArrayField(
        models.DateField(),
        default=list,  
        blank=True,
        null=True,
    )

    projected_points  = ArrayField(
        models.FloatField(),
        default=list,  
        blank=True,
        null=True,
    )

    actual_points = ArrayField(
        models.FloatField(),
        default=list,  
        blank=True,
        null=True,
    )

    def clean(self):
        super().clean()
        
        # Validate focus_area for food goals
        if self.goal_type == self.FOOD:
            valid_food_choices = [choice[0] for choice in self.FOOD_FOCUS_CHOICES]
            if self.focus_area not in valid_food_choices:
                raise ValidationError({
                    'focus_area': f'Invalid focus area for food goal. Must be one of: {", ".join(valid_food_choices)}'
                })

        # Validate objective conditions
        if self.objective == self.INCREASE and self.future_amount <= self.current_amount:
            raise ValidationError({
                'future_amount': 'For "INCREASE" objective, future_amount must be greater than current_amount.'
            })
        elif self.objective == self.DECREASE and self.future_amount >= self.current_amount:
            raise ValidationError({
                'future_amount': 'For "DECREASE" objective, future_amount must be less than current_amount.'
            })
        elif self.objective == self.SAME:
            if self.current_amount != self.future_amount:
                # If SAME is selected but current and future are different, set them to the same value
                # You can also raise an error here if you prefer
                self.future_amount = self.current_amount
            # For SAME objective, you could also set current_amount and future_amount to a single provided value
            # This part depends on how you want to handle input for SAME objective
            # For example, if you have a separate field for the constant value:
            # self.current_amount = self.constant_value
            # self.future_amount = self.constant_value

    def save(self, *args, **kwargs):
        self.clean()  # Ensure clean is called before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_goal_type_display()} {self.get_pace_type_display()}"