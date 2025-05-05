from django.shortcuts import render,redirect,get_object_or_404
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
    return render(request, 'trajectory_chart.html')
def trajectory_chart(request, trajectory_id):

    # Fetch the specific trajectory
    trajectory = get_object_or_404(Trajectory, id=trajectory_id)
    
    # Prepare data for the chart
    labels = [point.strftime('%Y-%m-%d') for point in trajectory.timestamps]
    data = trajectory.projected_points
    
    # Convert data to JSON format
    data_json = json.dumps(data)
    labels_json = json.dumps(labels)
    
    # Pass data to the template
    return render(request, 'trajectories/trajectory_chart.html', {
        'data': data_json,
        'labels': labels_json,
    })

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
            # Print validation errors to the console/server log
            print(form.errors)
    else:
        form = TrajectoryForm()
    return render(request, 'trajectories/log_trajectory.html', {'form': form})




def update_trajectory(request):
    return HttpResponse("Based on how analytics change the trajectory will also be updated")