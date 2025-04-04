from django.db import models

# Create your models here.
class Analytics(models.Model):
    metric_name = models.CharField(max_length=50)
    period_type = models.CharField(max_length=50)
    current_value = models.IntegerField()
    previous_value = models.IntegerField()

    def __str__(self):
        return f"{self.metric_name} : {self.period_type}" 
