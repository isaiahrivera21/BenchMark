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


def generate_dates(start_date, total_intervals, interval_type):
    dates = []
    current_date = start_date

    for t in range(total_intervals + 1):
        dates.append(current_date)

        if interval_type == "DAILY":
            current_date += timedelta(days=1)
        elif interval_type == "WEEKLY":
            current_date += timedelta(weeks=1)
        elif interval_type == "MONTHLY":
            current_date += timedelta(days=30)

    return dates


# A --> current point
# B --> Where you want to be
def generate_trajectory(A, B, total_intervals, interval_type):
    trajectory = []

    if interval_type not in ["INCREASE", "DECREASE", "SAME"]:
        raise ValueError(
            f"Invalid interval_type: {interval_type}. Must be 'INCREASE', 'DECREASE', or 'SAME'."
        )

    for t in range(total_intervals + 1):
        if interval_type == "INCREASE":
            y = A + (B - A) * np.log(t + 1) / np.log(total_intervals + 1)
        elif interval_type == "DECREASE":
            if B >= A:
                raise ValueError("For 'DECREASE' type, B must be less than A.")
            y = A - (A - B) * np.log(t + 1) / np.log(total_intervals + 1)
        elif interval_type == "SAME":
            y = A

        trajectory.append(y)

    return trajectory


@receiver(post_save, sender=Trajectory)
def generate_trajectory_data(sender, instance, created, **kwargs):

    if created and instance.user:
        total_days = (instance.target_date - instance.start_date).days

        # Adjust total_intervals based on interval type
        if instance.pace_type == "DAILY":
            total_intervals = total_days
        elif instance.pace_type == "WEEKLY":
            total_intervals = total_days // 7
        elif instance.pace_type == "MONTHLY":
            total_intervals = total_days // 30

        instance.projected_points = generate_trajectory(
            instance.current_amount,
            instance.future_amount,
            total_intervals,
            instance.objective,
        )
        instance.timestamps = generate_dates(
            instance.start_date, total_intervals, instance.pace_type
        )
        instance.save()


@receiver(post_save, sender=UserLoggedExercise)
def update_exercise_tracking(sender, instance, created, **kwargs):
    if created and instance.user:
        logged_date = instance.exercise_logged_at.date()

        active_trajectories = Trajectory.objects.filter(
            user=instance.user, goal_type="EXERCISE", focus_area=instance.exercise_name
        )

        for trajectory in active_trajectories:
            latest_volume = (
                Analytics.objects.filter(
                    user=instance.user,
                    metric_name="Volume",
                    item_name=instance.exercise_name,
                )
                .order_by("-id")
                .first()
            )

            A = latest_volume.value if latest_volume else 0
            B = trajectory.future_amount
            interval_type = trajectory.objective

            total_days = (trajectory.target_date - logged_date).days

            if trajectory.pace_type == "DAILY":
                total_intervals = total_days
            elif trajectory.pace_type == "WEEKLY":
                total_intervals = total_days // 7
            elif trajectory.pace_type == "MONTHLY":
                total_intervals = total_days // 30

            generated_points = generate_trajectory(A, B, total_intervals, interval_type)

            trajectory.actual_points = generated_points
            trajectory.save()


@receiver(post_save, sender=UserLoggedFood)
def update_food_tracking(sender, instance, created, **kwargs):
    if created and instance.user:
        logged_date = instance.food_logged_at.date()

        active_trajectories = Trajectory.objects.filter(
            user=instance.user,
            goal_type="FOOD",
            start_date__lte=logged_date,
            target_date__gte=logged_date,
        )

        for trajectory in active_trajectories:
            focus_field_map = {
                "CALORIES": "calories",
                "FAT": "fat",
                "CARBOHYDRATES": "carbohydrates",
                "PROTEIN": "proten",
                "CHOLESTEROL": "cholesterol",
                "SODIUM": "sodium",
                "SUGAR": "sugar",
            }

            field_name = focus_field_map.get(trajectory.focus_area)

            if field_name:
                value = getattr(instance, field_name, 0)

                total_days = (trajectory.target_date - logged_date).days

                if trajectory.pace_type == "DAILY":
                    total_intervals = total_days
                elif trajectory.pace_type == "WEEKLY":
                    total_intervals = total_days // 7
                elif trajectory.pace_type == "MONTHLY":
                    total_intervals = total_days // 30

                if trajectory.objective == "INCREASE":
                    generated_points = generate_trajectory(
                        value, trajectory.future_amount, total_intervals, "INCREASE"
                    )
                elif trajectory.objective == "DECREASE":
                    generated_points = generate_trajectory(
                        value, trajectory.future_amount, total_intervals, "DECREASE"
                    )
                else:  # SAME
                    generated_points = generate_trajectory(
                        value, value, total_intervals, "SAME"
                    )

                trajectory.actual_points = generated_points
                trajectory.save()
