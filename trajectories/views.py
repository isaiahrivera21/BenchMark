from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import TrajectoryForm
from .models import Trajectory

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the trajectories index.")

@login_required
def create_trajectory(request):

    if request.method == 'POST':
        form = TrajectoryForm(request.POST)
        if form.is_valid():
            trajectory = form.save(commit=False)
            trajectory.user = request.user  # Assuming you have a user field in your model
            trajectory.save()
            return redirect('index')  # Redirect to a list of trajectories or another page
    else:
        form = TrajectoryForm()
    return render(request, 'trajectories/log_trajectory.html', {'form': form})


def update_trajectory(request):
    return HttpResponse("Based on how analytics change the trajectory will also be updated")