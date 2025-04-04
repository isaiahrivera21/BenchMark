from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .forms import UserLoggedExerciseForm
from .models import UserLoggedExercise
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    return HttpResponse("Hello, world. You're at the exercise_logging index.")

@login_required
def log_exercise(request):
    if request.method == 'POST':
        form = UserLoggedExerciseForm(request.POST) # create form instance

        # check if valid
        if form.is_valid():
            user_logged_exercise = form.save(commit=False)
            user_logged_exercise.user = request.user
            user_logged_exercise.save()
            return redirect('/exerciselogging/create')
        
    else:
        form = UserLoggedExerciseForm()  # Empty form for GET requests
        return render(request,"exerciselogging/logexercise.html", {"form": form})

    # return HttpResponse("This function will post the food the user logged to the database")

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


