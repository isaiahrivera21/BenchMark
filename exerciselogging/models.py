from django.db import models
from user.models import CustomUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class UserLoggedExercise(models.Model):
    exercise_name = models.CharField(max_length=200)
    exercise_logged_at = models.DateTimeField("exercise date")
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.IntegerField()
    notes = models.CharField(max_length=200,null=True, blank=True)
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True) # we care about which user logged this food
    target_muscles = ArrayField(models.CharField(max_length=100), blank=True,null=True)


    def __str__(self):
        return f"{self.exercise_name} {self.sets}X{self.reps} ({self.weight})"