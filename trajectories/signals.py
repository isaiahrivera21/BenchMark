from django.db.models.signals import post_save
from django.dispatch import receiver
from exerciselogging.models import UserLoggedExercise
from foodlogging.models import UserLoggedFood
from .models import Trajectory
from analytics.models import Analytics
from django.utils import timezone
from datetime import timedelta
import numpy as np
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Function to generate dates based on the interval
def generate_dates(start_date, total_intervals, interval_type):
    dates = []
    current_date = start_date
    
    for t in range(total_intervals + 1):
        dates.append(current_date)
        
        if interval_type == 'DAILY':
            current_date += timedelta(days=1)
        elif interval_type == 'WEEKLY':
            current_date += timedelta(weeks=1)
        elif interval_type == 'MONTHLY':
            # Assuming approximately 30 days per month
            current_date += timedelta(days=30)
    
    return dates

# A --> current point 
# B --> Where you want to be 
def generate_trajectory(A, B, total_intervals, interval_type):
    trajectory = []
    
    if interval_type not in ['INCREASE', 'DECREASE', 'SAME']:
        raise ValueError(f"Invalid interval_type: {interval_type}. Must be 'INCREASE', 'DECREASE', or 'SAME'.")
    
    for t in range(total_intervals + 1):
        if interval_type == 'INCREASE':
            y = A + (B - A) * np.log(t + 1) / np.log(total_intervals + 1)
        elif interval_type == 'DECREASE':
            if B >= A:
                raise ValueError("For 'DECREASE' type, B must be less than A.")
            y = A - (A - B) * np.log(t + 1) / np.log(total_intervals + 1)
        elif interval_type == 'SAME':
            y = A
        
        trajectory.append(y)
    
    return trajectory


@receiver(post_save, sender=Trajectory)
def generate_trajectory_data(sender, instance, created, **kwargs):
    # after a trajectory is made we want to populate the arrays so that we actually have the trajectories

    # check if it is increasing decrasing or the same 

    if created and instance.user:
        # Calculate total duration in days
        # start_date = instance.start_date.date()
        total_days = (instance.target_date - instance.start_date).days

        # Adjust total_intervals based on interval type
        if instance.pace_type == 'DAILY':
            total_intervals = total_days
        elif instance.pace_type == 'WEEKLY':
            total_intervals = total_days // 7  # Convert days to weeks
        elif instance.pace_type == 'MONTHLY':
            total_intervals = total_days // 30  # Approximate a month as 30 days

        instance.projected_points = generate_trajectory(instance.current_amount, instance.future_amount, total_intervals,instance.objective)
        instance.timestamps = generate_dates(instance.start_date, total_intervals, instance.pace_type)
        instance.save() 
        

@receiver(post_save, sender=UserLoggedExercise)
def update_exercise_trajectory(sender, instance, created, **kwargs):
    pass

@receiver(post_save, sender=UserLoggedFood)
def update_food_trajectory(sender, instance, created, **kwargs):
    pass

