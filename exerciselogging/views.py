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

import inflect  # Install this package: pip install inflect

def normalize_exercise_name(name):
    # Convert to lowercase
    name = name.lower()
    
    # Replace hyphens and underscores with spaces
    name = re.sub(r'[-_]', ' ', name)
    
    # Split camelCase into words
    name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
    
    # Capitalize each word
    name = name.title()
    
    return name

def index(request):
    return HttpResponse("Hello, world. You're at the exercise_logging index.")


@login_required
def exercise_homepage(request):
    # Get all unique exercise names for the current user
    unique_exercises = UserLoggedExercise.objects.filter(user=request.user).values_list('exercise_name', flat=True).distinct()
    
    context = {
        'unique_exercises': unique_exercises
    }
    
    return render(request, 'exerciselogging/exercise_homepage.html', context)

@login_required
def exercise_detail(request, exercise_name):
    # Get all logs for the specified exercise and current user
    exercise_logs = UserLoggedExercise.objects.filter(
        user=request.user,
        exercise_name=exercise_name
    ).order_by('-exercise_logged_at')  # Order by date descending
    
    context = {
        'exercise_name': exercise_name,
        'exercise_logs': exercise_logs
    }
    
    return render(request, 'exerciselogging/exercise_detail.html', context)

@login_required
def log_exercise(request):
    if request.method == 'POST':
        form = UserLoggedExerciseForm(request.POST)
        
        if form.is_valid():
            user_logged_exercise = form.save(commit=False)
            user_logged_exercise.user = request.user
            user_logged_exercise.save()
            return redirect(reverse('exercise_detail', kwargs={'exercise_name': user_logged_exercise.exercise_name}))
    
    else:
        # Check if exercise_name is provided in the URL parameters
        exercise_name = request.GET.get('exercise_name', None)
        initial_data = {'exercise_name': exercise_name} if exercise_name else None
        form = UserLoggedExerciseForm(initial=initial_data)
    
    return render(request, 'exerciselogging/logexercise.html', {'form': form})

@login_required
def edit_exercise(request,id):
    exercise = get_object_or_404(UserLoggedExercise, id=id)
    # entry = UserLoggedExercise.objects.get(id)

    if request.method == 'POST':
        form = UserLoggedExerciseForm(request.POST,instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('/exerciselogging/create')
    else:
        form = UserLoggedExerciseForm(instance=exercise)

    return render(request,"exerciselogging/editexercise.html",{"form": form, "exercise": exercise})

@login_required
def delete_exercise(request,id):
    exercise = get_object_or_404(UserLoggedExercise, id=id)
    if request.method == 'POST':

        # Delete the exercise
        exercise.delete()
        
        return redirect('/exerciselogging/create')
    
    return render(request, "exerciselogging/deleteexercise.html", {"exercise": exercise})
    # context --> data to pass to the template 

# this will probably need a user id

@login_required
def list_all_exercise(request):
    exercises = UserLoggedExercise.objects.filter(user=request.user)
    # paginator = Paginator(exercises, 10)  # Show 10 exercises per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    return render(request, 'exerciselogging/list_all_exercise.html', {'exercises': exercises})


