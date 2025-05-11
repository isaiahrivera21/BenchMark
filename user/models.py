from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class CustomUser(AbstractUser):  # Inherit from AbstractUser
    M = "METRIC"
    I = "IMPERIAL"

    PACE_CHOICES = [
        (M, "Metric"),
        (I, "Imperial (U.S.)"),
    ]

    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]

    ACTIVITY_CHOICES = [
        (1.2, "Sedentary (little to no exercise)"),
        (1.375, "Lightly active (light exercise 1-3 days/week)"),
        (1.55, "Moderately active (moderate exercise 3-5 days/week)"),
        (1.725, "Very active (hard exercise 6-7 days/week)"),
        (1.9, "Super active (very hard exercise & physical job)"),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True)  # Allow empty values
    activity_level = models.FloatField(choices=ACTIVITY_CHOICES, blank=True, null=True)

    weight_log = ArrayField(base_field=models.FloatField(), blank=True, null=True)

    weight_log_dates = ArrayField(base_field=models.DateField(), blank=True, null=True)

    steps_log = ArrayField(base_field=models.IntegerField(), blank=True, null=True)

    steps_log_dates = ArrayField(base_field=models.DateField(), blank=True, null=True)

    age = models.IntegerField(null=True, blank=True)
    pace_unit = models.CharField(
        max_length=10, choices=PACE_CHOICES, default=M, null=True, blank=True
    )

    def __str__(self):
        return self.username
