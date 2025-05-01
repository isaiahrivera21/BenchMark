from django.db import models

# Create your models here.
class FoodEntry(models.Model):
    food_name = models.CharField(max_length=200)
    calories = models.IntegerField()
    fat = models.IntegerField(null=True, blank=True)
    carbohydrates = models.IntegerField(null=True, blank=True)
    protein = models.IntegerField(null=True, blank=True)
    cholesterol = models.IntegerField(null=True, blank=True)
    sodium = models.IntegerField(null=True, blank=True)
    sugar = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.food_name}"
    