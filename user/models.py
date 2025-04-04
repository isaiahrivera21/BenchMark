from django.db import models

# Create your models here.
# class User(models.Model):
#     M = "METRIC"
#     I = "IMPERIAL"

#     # first is what is actually set in the model second is the human readable form 
#     PACE_CHOICES = [
#     (M, "Metric"),
#     (I, "Imperial (U.S.)"),
#     ]   

#     username = models.CharField(max_length=200)
#     height = models.IntegerField()
#     weight = models.IntegerField()
#     age = models.IntegerField()

#     def __str__(self):
#         return self.username

# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):  # Inherit from AbstractUser
    M = "METRIC"
    I = "IMPERIAL"

    PACE_CHOICES = [
        (M, "Metric"),
        (I, "Imperial (U.S.)"),
    ]

    height = models.FloatField(null=True, blank=True)  # Allow empty values
    weight = models.FloatField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    pace_unit = models.CharField(
        max_length=10,
        choices=PACE_CHOICES,
        default=M
    )

    def __str__(self):
        return self.username
