from django.db import models

# Create your models here.
class FoodEntry(models.Model):
    food_name = models.CharField(max_length=200)
    calories = models.IntegerField()
    fat = models.IntegerField(null=True, blank=True)
    carbohydrates = models.IntegerField(null=True, blank=True)
    protien = models.IntegerField(null=True, blank=True)
    cholestorol = models.IntegerField(null=True, blank=True)
    sodium = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.food_name}"
    