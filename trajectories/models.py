from django.db import models

# Create your models here.
class Question(models.Model):
    D = "DAILY"
    W = "WEEKLY"
    M = "MONTHLY"
    Y = "YEARLY"

    # first is what is actually set in the model second is the human readable form 
    PACE_CHOICES = [
    (D, "Daily"),
    (W, "Weekly"),
    (M, "Monthly"),
    (Y, "Yearly"),
    ]   

    type = models.CharField(max_length=50)
    pace_type = models.CharField(max_length=50,choices=PACE_CHOICES)
    cur_value = models.IntegerField()
    goal_value = models.IntegerField()
    improvement = models.FloatField()
    target_date = models.DateField("target date")

    def __str__(self):
        return f"{self.type} {self.pace_type}"