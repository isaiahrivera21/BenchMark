from django.db import models
from user.models import CustomUser

# Create your models here.
class UserLoggedFood(models.Model):

    B = "BREAKFAST"
    L = "LUNCH"
    D = "DINNER"
    S = "SNACK"

    # first is what is actually set in the model second is the human readable form 
    MEAL_CHOICES = [
    (B, "Breakfast"),
    (L, "Lunch"),
    (D, "Dinner"),
    (S, "Snack"),
    ]   

    food_name = models.CharField(max_length=200)
    food_logged_at = models.DateTimeField(auto_now_add=True)
    meal_type = models.CharField(choices=MEAL_CHOICES)
    serving_size = models.IntegerField() # should probably set to a default value of 1 
    calories = models.IntegerField()
    fat = models.IntegerField(null=True, blank=True)
    carbohydrates = models.IntegerField(null=True, blank=True)
    protien = models.IntegerField(null=True, blank=True)
    cholestorol = models.IntegerField(null=True, blank=True)
    sodium = models.IntegerField(null=True, blank=True)
    sugar = models.IntegerField(null=True, blank=True)
    
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.meal_type} {self.food_name}"
    
    
