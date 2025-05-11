from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .forms import UserLoggedExerciseForm
from .models import UserLoggedExercise
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import re
from django.urls import reverse
import json
from trajectories.models import Trajectory
from analytics.models import Analytics
from django.http import JsonResponse
from exerciserepo.models import ExerciseEntry
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from exerciselogging.models import UserLoggedExercise
from analytics.models import Analytics


def normalize_exercise_name(name):
    name = name.lower()

    # Replace hyphens and underscores with spaces
    name = re.sub(r"[-_]", " ", name)

    # Split camelCase into words
    name = re.sub(r"(?<!^)(?=[A-Z])", " ", name)

    name = name.title()

    return name


def index(request):
    return HttpResponse("Hello, world. You're at the exercise_logging index.")


def exercise_autocomplete(request):
    query = request.GET.get("query", "")
    results = []
    if query:
        exercise_entries = ExerciseEntry.objects.filter(
            exercise_name__startswith=query
        )[:10]
        results = [
            {
                "name": entry.exercise_name,
                "target_muscles": entry.target_muscles,
            }
            for entry in exercise_entries
        ]
    return JsonResponse({"results": results})


@login_required
def exercise_homepage(request):
    unique_exercises = (
        UserLoggedExercise.objects.filter(user=request.user)
        .values_list("exercise_name", flat=True)
        .distinct()
    )

    exercise_trajectories = Trajectory.objects.filter(
        user=request.user, goal_type="EXERCISE"
    )

    for trajectory in exercise_trajectories:
        # Convert timestamps to string format
        trajectory.labels = json.dumps(
            [point.strftime("%Y-%m-%d") for point in trajectory.timestamps]
        )

        trajectory.data = json.dumps(trajectory.projected_points)

    context = {
        "unique_exercises": unique_exercises,
        "exercise_trajectories": exercise_trajectories,
    }

    return render(request, "exerciselogging/exercise_homepage.html", context)


@login_required
def exercise_detail(request, exercise_name):
    exercise_logs = UserLoggedExercise.objects.filter(
        user=request.user, exercise_name=exercise_name
    ).order_by("-exercise_logged_at")

    metrics = ["Volume", "Weight/Rep", "Rep Change", "Set Change"]

    # Fetch the latest analytics for each metric related to this exercise
    latest_analytics = []
    for metric in metrics:
        try:
            analytic = Analytics.objects.filter(
                user=request.user, item_name=exercise_name, metric_name=metric
            ).latest("id")
            latest_analytics.append(
                {"metric_name": analytic.metric_name, "value": analytic.value}
            )
        except Analytics.DoesNotExist:
            latest_analytics.append(
                {"metric_name": metric, "value": "No data available"}
            )

    context = {
        "exercise_name": exercise_name,
        "exercise_logs": exercise_logs,
        "latest_analytics": latest_analytics,
    }

    return render(request, "exerciselogging/exercise_detail.html", context)


@login_required
def log_exercise(request):
    if request.method == "POST":
        form = UserLoggedExerciseForm(request.POST)

        if form.is_valid():
            user_logged_exercise = form.save(commit=False)
            user_logged_exercise.user = request.user
            user_logged_exercise.exercise_name = normalize_exercise_name(
                user_logged_exercise.exercise_name
            )
            user_logged_exercise.save()
            return redirect(
                reverse(
                    "exercise_detail",
                    kwargs={"exercise_name": user_logged_exercise.exercise_name},
                )
            )
        else:
            print(form.errors)
            return render(request, "exerciselogging/logexercise.html", {"form": form})

    else:
        exercise_name = request.GET.get("exercise_name", None)
        initial_data = {"exercise_name": exercise_name} if exercise_name else None
        form = UserLoggedExerciseForm(initial=initial_data)

    return render(request, "exerciselogging/logexercise.html", {"form": form})


@login_required
def edit_exercise(request, id):
    exercise = get_object_or_404(UserLoggedExercise, id=id)

    if request.method == "POST":
        form = UserLoggedExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect("/exercise")
    else:
        form = UserLoggedExerciseForm(instance=exercise)

    return render(
        request,
        "exerciselogging/editexercise.html",
        {"form": form, "exercise": exercise},
    )


@login_required
def delete_exercise(request, id):
    exercise = get_object_or_404(UserLoggedExercise, id=id)
    if request.method == "POST":

        # Delete the exercise
        exercise.delete()

        return redirect("/exerciselogging/create")

    return render(
        request, "exerciselogging/deleteexercise.html", {"exercise": exercise}
    )


@login_required
def list_all_exercise(request):
    exercises = UserLoggedExercise.objects.filter(user=request.user)

    return render(
        request, "exerciselogging/list_all_exercise.html", {"exercises": exercises}
    )
