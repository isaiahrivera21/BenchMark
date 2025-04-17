# from django.db import models

# # Create your models here.
# class Trajectory(models.Model):
#     D = "DAILY"
#     W = "WEEKLY"
#     M = "MONTHLY"
#     Y = "YEARLY"

#     # first is what is actually set in the model second is the human readable form 
#     PACE_CHOICES = [
#     (D, "Daily"),
#     (W, "Weekly"),
#     (M, "Monthly"),
#     (Y, "Yearly"),
#     ]  

#     INC = "INCREASE"
#     DEC = "DECREASE"
#     SAME = "SAME"

#     OBJECTIVE_CHOICES = [
#     (INC, "Increase"),
#     (DEC, "Decrease"),
#     (SAME, "Same")
#     ]

#     pace_type = models.CharField(max_length=50,choices=PACE_CHOICES) # this will be set by logic 
#     start_date = models.DateTimeField(auto_now_add=True)
#     target_date = models.DateField("target date")
#     amount = models.IntegerField()
#     objective = models.CharField(max_length=50,choices=OBJECTIVE_CHOICES) 
#     focus_area = "?"
    

#     def __str__(self):
#         return f"{self.type} {self.pace_type}"

from django.db import models
from django.core.exceptions import ValidationError
from user.models import CustomUser

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
        ('CHOLESTOROL','cholestorol')

    ]

    pace_type = models.CharField(max_length=50, choices=PACE_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    target_date = models.DateField("Target Date")
    amount = models.IntegerField()
    objective = models.CharField(max_length=50, choices=OBJECTIVE_CHOICES)
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPE_CHOICES)
    focus_area = models.TextField()  # Will be either dropdown choice or free text
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)

    def clean(self):
        super().clean()
        
        if self.goal_type == self.FOOD:
            valid_food_choices = [choice[0] for choice in self.FOOD_FOCUS_CHOICES]
            if self.focus_area not in valid_food_choices:
                raise ValidationError({
                    'focus_area': f'Invalid focus area for food goal. Must be one of: {", ".join(valid_food_choices)}'
                })

    def __str__(self):
        return f"{self.get_goal_type_display()} {self.get_pace_type_display()}"