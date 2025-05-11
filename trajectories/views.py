from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TrajectoryForm
from .models import Trajectory
from django.http import JsonResponse


# Create your views here.
from django.http import HttpResponse
import json


def index(request):
    return HttpResponse("Hello, world. You're at the trajectories index.")


def trajectory_chart(request):
    return render(request, "trajectory_chart.html")


def trajectory_chart(request, trajectory_id):
    trajectory = get_object_or_404(Trajectory, id=trajectory_id)

    labels = [point.strftime("%Y-%m-%d") for point in trajectory.timestamps]
    data = trajectory.projected_points

    data_json = json.dumps(data)
    labels_json = json.dumps(labels)

    return render(
        request,
        "trajectories/trajectory_chart.html",
        {
            "data": data_json,
            "labels": labels_json,
        },
    )


@login_required
def create_trajectory(request):

    if request.method == "POST":
        form = TrajectoryForm(request.POST)
        if form.is_valid():
            trajectory = form.save(commit=False)
            trajectory.user = request.user
            trajectory.save()
            return redirect("index")

        else:
            print(form.errors)
    else:
        form = TrajectoryForm()
    return render(request, "trajectories/log_trajectory.html", {"form": form})


def update_trajectory(request):
    return HttpResponse(
        "Based on how analytics change the trajectory will also be updated"
    )
