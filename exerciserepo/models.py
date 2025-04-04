from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class ExerciseEntry(models.Model):
    exercise_name = models.CharField(max_length=200)
    target_muscles = ArrayField(models.CharField(max_length=100), blank=True)


    def __str__(self):
        return f"{self.exercise_name}"