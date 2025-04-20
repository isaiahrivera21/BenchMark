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

# NOTE: Edit the templates to work for food. 

def index(request):
    return HttpResponse("Hello, world. You're at the food_logging index.")

@login_required
def food_homepage(request):
    # Fetch the latest daily and monthly analytics based on highest ID
    try:
        latest_daily = Analytics.objects.filter(
            user=request.user,
            period_type='Daily'
        ).latest('id')
    except Analytics.DoesNotExist:
        latest_daily = None

    try:
        latest_monthly = Analytics.objects.filter(
            user=request.user,
            period_type='Monthly'
        ).latest('id')
    except Analytics.DoesNotExist:
        latest_monthly = None

    # Fetch all food-related trajectories
    food_trajectories = Trajectory.objects.filter(
        user=request.user,
        goal_type='FOOD'
    )

    # Prepare data for each trajectory
    for trajectory in food_trajectories:
        # Convert timestamps to string format
        trajectory.labels = json.dumps([point.strftime('%Y-%m-%d') for point in trajectory.timestamps])
        # Convert projected points to a serializable format
        trajectory.data = json.dumps(trajectory.projected_points)

    context = {
        'latest_daily': latest_daily,
        'latest_monthly': latest_monthly,
        'food_trajectories': food_trajectories,
    }

    return render(request, 'foodlogging/food_homepage.html', context)

@login_required
def log_food(request):
    # pretty sure I define the functionality here

    if request.method == 'POST':
        form = UserLoggedFoodForm(request.POST) # create form instance

        # check if valid
        if form.is_valid():
            user_logged_food = form.save(commit=False)
            user_logged_food.user = request.user
            user_logged_food.save()
            return redirect('/foodlogging/create')
    else:
        form = UserLoggedFoodForm()
        return render(request,"foodlogging/logfood.html", {"form": form})

@login_required
def edit_food(request,id):
    food = get_object_or_404(UserLoggedFood, id=id)
    # entry = UserLoggedFood.objects.get(id)

    if request.method == 'POST':
        form = UserLoggedFoodForm(request.POST,instance=food)
        if form.is_valid():
            form.save()
            return redirect('/foodlogging/create')
    else:
        form = UserLoggedFoodForm(instance=food)

    return render(request,"foodlogging/editfood.html",{"form": form, "food": food})

@login_required
def delete_food(request,id):
    food = get_object_or_404(UserLoggedFood, id=id)
    if request.method == 'POST':

        # Delete the food
        food.delete()
        
        return redirect('/foodlogging/create')
    
    return render(request, "foodlogging/deletefood.html", {"food": food})

@login_required
def list_all_food(request):
    foods = UserLoggedFood.objects.filter(user=request.user)
    return render(request, 'foodlogging/list_all_food.html', {'foods': foods}) 
