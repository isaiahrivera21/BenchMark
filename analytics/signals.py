from django.db.models.signals import post_save
from django.dispatch import receiver
from exerciselogging.models import UserLoggedExercise
from foodlogging.models import UserLoggedFood
from user.models import CustomUser
from .models import Analytics
from django.utils import timezone
from datetime import timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Avg
from django.db.models import Sum


def create_exercise_metric(metric_name, metric_value, user, item):

    Analytics.objects.create(
        metric_name=metric_name,
        period_type="Session",
        value=metric_value,
        value_type="Percentage",
        user=user,
        item_name=item,
    )


def create_average_macro_metric(user, foods, time_range):
    if not foods.exists():
        return

    averages = foods.aggregate(
        avg_calories=Avg("calories"),
        avg_fat=Avg("fat"),
        avg_carbohydrates=Avg("carbohydrates"),
        avg_protien=Avg("protien"),
        avg_cholesterol=Avg("cholestorol"),
        avg_sodium=Avg("sodium"),
        avg_sugar=Avg("sugar"),
    )

    Analytics.objects.create(
        metric_name=f"Average {time_range} Calories",
        period_type=time_range,
        value=averages["avg_calories"],
        value_type="Numerical",
        user=user,
        item_name="",
    )

    return averages


@receiver(post_save, sender=UserLoggedExercise)
def generate_exercise_metric(sender, instance, created, **kwargs):
    if created and instance.user:
        logs = UserLoggedExercise.objects.filter(
            user=instance.user,
            exercise_name__iexact=instance.exercise_name,  # Case-insensitive match
        ).order_by("-exercise_logged_at")

        if logs.count() >= 2:
            latest_log = logs[0]
            previous_log = logs[1]

            l_sets = latest_log.sets
            l_reps = latest_log.reps
            l_weight = latest_log.weight

            p_sets = previous_log.sets
            p_reps = previous_log.reps
            p_weight = previous_log.weight

            volume_change = (l_sets * l_reps * l_weight) / (p_sets * p_reps * p_weight)
            create_exercise_metric(
                "Volume", volume_change, instance.user, instance.exercise_name
            )

            weight_per_rep_change = (l_weight / l_reps) / (p_weight / p_reps)
            create_exercise_metric(
                "Weigth/Rep",
                weight_per_rep_change,
                instance.user,
                instance.exercise_name,
            )

            rep_change = l_reps / p_reps
            create_exercise_metric(
                "Rep Change", rep_change, instance.user, instance.exercise_name
            )

            set_change = l_sets / p_sets
            create_exercise_metric(
                "Set Change", set_change, instance.user, instance.exercise_name
            )

            metrics_data = {
                "volume_change": volume_change,
                "weight_per_rep_change": weight_per_rep_change,
                "rep_change": rep_change,
                "set_change": set_change,
            }

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "metrics_updates", {"type": "metrics.update", "message": metrics_data}
            )


@receiver(post_save, sender=UserLoggedFood)
def generate_average_macro_consumption(sender, instance, created, **kwargs):

    if created and instance.user:
        user = instance.user

        # 1) All-time average
        all_time_foods = UserLoggedFood.objects.filter(user=user)
        all_time_averages = create_average_macro_metric(user, all_time_foods, "Daily")

        # 2) Weekly average (past 7 days)
        one_week_ago = timezone.now() - timedelta(days=7)
        weekly_foods = UserLoggedFood.objects.filter(
            user=user, food_logged_at__gte=one_week_ago
        )
        weekly_averages = create_average_macro_metric(user, weekly_foods, "Weekly")

        # 3) Monthly average (past 30 days)
        one_month_ago = timezone.now() - timedelta(days=30)
        monthly_foods = UserLoggedFood.objects.filter(
            user=user, food_logged_at__gte=one_month_ago
        )
        monthly_averages = create_average_macro_metric(user, monthly_foods, "Monthly")

        all_time_food_data = {
            "average_calories": all_time_averages["avg_calories"],
            "average_fat": all_time_averages["avg_fat"],
            "average_carbohydrates": all_time_averages["avg_carbohydrates"],
            "average_protien": all_time_averages["avg_protien"],
            "average_cholesterol": all_time_averages["avg_cholesterol"],
            "average_sodium": all_time_averages["avg_sodium"],
            "average_sugar": all_time_averages["avg_sugar"],
        }

        weekly_food_data = {
            "average_calories": weekly_averages["avg_calories"],
            "average_fat": weekly_averages["avg_fat"],
            "average_carbohydrates": weekly_averages["avg_carbohydrates"],
            "average_protien": weekly_averages["avg_protien"],
            "average_cholesterol": weekly_averages["avg_cholesterol"],
            "average_sodium": weekly_averages["avg_sodium"],
            "average_sugar": weekly_averages["avg_sugar"],
        }

        monthly_food_data = {
            "average_calories": monthly_averages["avg_calories"],
            "average_fat": monthly_averages["avg_fat"],
            "average_carbohydrates": monthly_averages["avg_carbohydrates"],
            "average_protien": monthly_averages["avg_protien"],
            "average_cholesterol": monthly_averages["avg_cholesterol"],
            "average_sodium": monthly_averages["avg_sodium"],
            "average_sugar": monthly_averages["avg_sugar"],
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "all_time_macros_updates",
            {"type": "all_time_macros.update", "message": all_time_food_data},
        )

        async_to_sync(channel_layer.group_send)(
            "weekly_macros_updates",
            {"type": "weekly_macros.update", "message": weekly_food_data},
        )

        async_to_sync(channel_layer.group_send)(
            "monthly_macros_updates",
            {"type": "monthly_macros.update", "message": monthly_food_data},
        )


@receiver(post_save, sender=UserLoggedFood)
@receiver(post_save, sender=UserLoggedExercise)
@receiver(post_save, sender=CustomUser)
def update_calorie_balance(sender, instance, created, **kwargs):
    today = timezone.now().date()
    MET = 3.6

    if sender in [UserLoggedFood, UserLoggedExercise]:
        user = instance.user
    elif sender == CustomUser:
        user = instance
    else:
        return

    gender = user.gender
    activity_factor = user.activity_level
    weight = user.weight_log[-1]

    if hasattr(user, "steps_log") and user.steps_log:
        steps_taken = user.steps_log[-1] if not created else 0
    else:
        steps_taken = 0

    age = user.age
    height = user.height

    if gender == "M":
        BMR = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        BMR = 10 * weight + 6.25 * height - 5 * age - 161

    exercises = UserLoggedExercise.objects.filter(
        user=user, exercise_logged_at__date=today
    )
    # exercise_logged_at__date=today <-- this is the reaosn why we are getting nothing

    if exercises.exists():
        first_exercise = exercises.earliest("exercise_logged_at").exercise_logged_at
        last_exercise = exercises.latest("exercise_logged_at").exercise_logged_at
        time = (
            last_exercise - first_exercise
        ).total_seconds() / 60  # Convert to minutes
    else:
        time = 0

    exercise_calories_burned = time * (MET * 3.5 * weight / 200)

    # formula: TDEE = (BMR × activity factor) + (steps taken × 0.04 × weight (kg)) + exercise calories burned.
    tdee = (BMR * activity_factor) + (steps_taken * 0.04) + (exercise_calories_burned)

    total_calories_consumed = (
        UserLoggedFood.objects.filter(user=user, food_logged_at__date=today).aggregate(
            Sum("calories")
        )["calories__sum"]
        or 0
    )

    calorie_balance = tdee

    print("BMR: ", BMR)
    print("weight: ", weight)
    print("height: ", height)
    print("steps_taken: ", steps_taken)
    print("time: ", time)
    print("total_calories: ", total_calories_consumed)
    print("exercises: ", exercises)
    print("tdee: ", tdee)

    Analytics.objects.create(
        metric_name="calorie_balance",
        period_type="Daily",
        value=calorie_balance,
        value_type="Numerical",
        user=user,
        item_name="",
    )


@receiver(post_save, sender=UserLoggedFood)
def daily_total_consumed_calories(sender, instance, **kwargs):

    today = timezone.now().date()
    user = instance.user

    total_calories_consumed = UserLoggedFood.objects.filter(
        user=user, food_logged_at__date=today
    ).aggregate(Sum("calories"))["calories__sum"]

    Analytics.objects.create(
        metric_name="daily_calories_consumed",
        period_type="Daily",
        value=total_calories_consumed,
        value_type="Numerical",
        user=user,
        item_name="",
    )
