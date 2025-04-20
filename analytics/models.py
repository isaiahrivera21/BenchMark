from django.db import models
from user.models import CustomUser

# Create your models here.
class Analytics(models.Model):

    P = "PERCENTAGE"
    N = "NUMERICAL"

    # seeing whether the metric is expressed as a percentage or a number 
    VALUE_TYPE_CHOICES = [
    (P, "Percentage"),
    (N, "Numerical")
    ]   

    D = "DAILY"
    W = "WEEKLY"
    M = "MONTHLY"
    S = "SESSION"

    PERIOD_TYPE_CHOICES = [
    (D, "Daily"),
    (W, "Weekly"),
    (M, "Monthly"),
    (S, "Session")
    ]   



    metric_name = models.CharField(max_length=50,null=False, blank=False)
    period_type = models.CharField(choices=PERIOD_TYPE_CHOICES,null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    value_type = models.CharField(choices=VALUE_TYPE_CHOICES,null=False, blank=False,default="Session")
    item_name = models.CharField(null=False, blank=True)
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.metric_name} : {self.period_type}" 
