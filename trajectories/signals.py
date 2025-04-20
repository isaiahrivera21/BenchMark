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
def update_exercise_tracking(sender, instance, created, **kwargs):
    if created and instance.user:
        
        # we have to querey for all trajectories associated with the thing we are trying to update (aka need to querey for focus area).
        # for exercises we need to querey for the specific name of that exercise. 


        # we need some logic here to check if we get a hit or not. If we don't just pass or exit

        # if we do hit we need to acess the weight sets or reps???? or do we acess something from analytics. For exercise its not specifically clear what they want to increase.
        # given that we only have one int for each I think for exercises we should just do trajectories based on volume. For expected we can have something that makes 
        # a change in the box to sets reps and weight BUT in the backend its gonna multiply out to be volume.

        # then for exercises with no weights we can measure just in reps and make sure to set weight and sets to 1. 
        pass
        


@receiver(post_save, sender=UserLoggedFood)
def update_food_tracking(sender, instance, created, **kwargs):
    if created and instance.user:
        # we have to querey for all trajectories associated with the thing we are trying to update (aka need to querey for focus area).
        # for food we specifically need to querey just to see if any of the macros listed have trajectories associated with them.
        

        # we need some logic here to check if we get a hit or not. If we don't just pass or exit

        # if we do have hit then we want to redo the total days calculation and send in a new starting point (wait I think I need to have something that records the total macros the user is consuming per day)
        # then the logic should change to whenever that specific thing changes instead of each logged food. 
        pass
