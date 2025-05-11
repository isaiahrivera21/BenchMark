from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .forms import UserLoggedFoodForm
from .models import UserLoggedFood
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from analytics.models import Analytics
from trajectories.models import Trajectory
import json
from django.http import JsonResponse
from foodrepo.models import FoodEntry
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from calendar import monthrange


def index(request):
    return HttpResponse("Hello, world. You're at the food_logging index.")


def food_autocomplete(request):
    query = request.GET.get("query", "")
    results = []
    if query:
        food_entries = FoodEntry.objects.filter(food_name__startswith=query)[:10]
        results = [
            {
                "id": entry.id,
                "name": entry.food_name,
                "calories": entry.calories,
                "fat": entry.fat,
                "carbohydrates": entry.carbohydrates,
                "protein": entry.protein,
                "cholesterol": entry.cholesterol,
                "sodium": entry.sodium,
                "sugar": entry.sugar,
            }
            for entry in food_entries
        ]
    return JsonResponse({"results": results})


@login_required
def food_homepage(request):
    try:
        daily_calories = Analytics.objects.filter(
            user=request.user,
            period_type="Daily",
            metric_name="daily_calories_consumed",
        ).latest("id")
    except Analytics.DoesNotExist:
        daily_calories = None

    try:
        calorie_balance = Analytics.objects.filter(
            user=request.user, period_type="Daily", metric_name="calorie_balance"
        ).latest("id")
    except Analytics.DoesNotExist:
        calorie_balance = None

    try:
        latest_monthly = Analytics.objects.filter(
            user=request.user, period_type="Monthly"
        ).latest("id")
    except Analytics.DoesNotExist:
        latest_monthly = None

    food_trajectories = Trajectory.objects.filter(user=request.user, goal_type="FOOD")

    for trajectory in food_trajectories:
        trajectory.labels = json.dumps(
            [point.strftime("%Y-%m-%d") for point in trajectory.timestamps]
        )
        trajectory.data = json.dumps(trajectory.projected_points)


@login_required
def food_homepage(request):
    try:
        daily_calories = Analytics.objects.filter(
            user=request.user,
            period_type="Daily",
            metric_name="daily_calories_consumed",
        ).latest("id")
    except Analytics.DoesNotExist:
        daily_calories = None

    try:
        calorie_balance = Analytics.objects.filter(
            user=request.user, period_type="Daily", metric_name="calorie_balance"
        ).latest("id")
    except Analytics.DoesNotExist:
        calorie_balance = None

    try:
        latest_monthly = Analytics.objects.filter(
            user=request.user, period_type="Monthly"
        ).latest("id")
    except Analytics.DoesNotExist:
        latest_monthly = None

    food_trajectories = Trajectory.objects.filter(user=request.user, goal_type="FOOD")

    for trajectory in food_trajectories:
        trajectory.labels = json.dumps(
            [point.strftime("%Y-%m-%d") for point in trajectory.timestamps]
        )
        trajectory.data = json.dumps(trajectory.projected_points)

    # Prepare data for calendar heatmap using UserLoggedFood
    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    daily_calorie_data = []
    current_date = first_day_of_month
    while current_date <= today:
        daily_logs = UserLoggedFood.objects.filter(
            user=request.user, food_logged_at__date=current_date
        )
        total_calories = sum(log.calories for log in daily_logs)

        color = (
            "#4CAF50"
            if total_calories < 1500
            else "#FFC107" if total_calories < 2500 else "#F44336"
        )
        daily_calorie_data.append(
            {
                "date": current_date.strftime("%Y-%m-%d"),
                "day": current_date.day,
                "calories": total_calories,
                "color": color,
            }
        )
        current_date += timedelta(days=1)

    # Prepare data for daily and monthly bar charts
    daily_chart_data = {
        "labels": [day["date"] for day in daily_calorie_data],
        "data": [day["calories"] for day in daily_calorie_data],
    }

    monthly_total = sum(day["calories"] for day in daily_calorie_data)

    context = {
        "daily_calories": daily_calories,
        "calorie_balance": calorie_balance,
        "latest_monthly": latest_monthly,
        "food_trajectories": food_trajectories,
        "daily_calorie_data": daily_calorie_data,
        "weekdays": weekdays,
        "daily_chart_data": json.dumps(daily_chart_data),
        "monthly_total": monthly_total,
    }

    return render(request, "foodlogging/food_homepage.html", context)


@login_required
def log_food(request):
    if request.method == "POST":
        form = UserLoggedFoodForm(request.POST)
        if form.is_valid():
            user_logged_food = form.save(commit=False)
            user_logged_food.user = request.user
            user_logged_food.save()
            return redirect("/food")
        else:
            # Return the form with errors
            return render(request, "foodlogging/logfood.html", {"form": form})
    else:
        form = UserLoggedFoodForm()
        return render(request, "foodlogging/logfood.html", {"form": form})


@login_required
def edit_food(request, id):
    food = get_object_or_404(UserLoggedFood, id=id)

    if request.method == "POST":
        form = UserLoggedFoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect("/food")
    else:
        form = UserLoggedFoodForm(instance=food)

    return render(request, "foodlogging/editfood.html", {"form": form, "food": food})


@login_required
def delete_food(request, id):
    food = get_object_or_404(UserLoggedFood, id=id)
    if request.method == "POST":

        # Delete the food
        food.delete()

        return redirect("/foodlogging/create")

    return render(request, "foodlogging/deletefood.html", {"food": food})


@login_required
def list_all_food(request):
    foods = UserLoggedFood.objects.filter(user=request.user)
    return render(request, "foodlogging/list_all_food.html", {"foods": foods})
