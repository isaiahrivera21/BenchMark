from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm  # Use default form
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import WeightEntryForm, StepsEntryForm

# so we want to render a form that just has two buttons that take you to one link or the other resectivly. Then probably in a header 1 something like this is the homepage. 
def homepage(request):
    return render(request, 'homepage/index.html')

@login_required
def log_weight(request):
    if request.method == 'POST':
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            
            # Get the current user
            user = request.user
            
            # Update weight log
            if user.weight_log is None:
                user.weight_log = []
            if user.weight_log_dates is None:
                user.weight_log_dates = []
            user.weight_log.append(weight)
            user.weight_log_dates.append(timezone.now().date())
            
            user.save()
            return redirect('')  #TODO: Redirect to home page
    else:
        form = WeightEntryForm()
    
    return render(request, 'homepage/log_weight.html', {'form': form})

@login_required
def log_steps(request):
    if request.method == 'POST':
        form = StepsEntryForm(request.POST)
        if form.is_valid():
            steps = form.cleaned_data['steps']
            
            # Get the current user
            user = request.user
            
            # Update steps log
            if user.steps_log is None:
                user.steps_log = []
            if user.steps_log_dates is None:
                user.steps_log_dates = []
            user.steps_log.append(steps)
            user.steps_log_dates.append(timezone.now().date())
            
            user.save()
            return redirect('')  # TODO: Redirect to home page 
    else:
        form = StepsEntryForm()
    
    return render(request, 'homepage/log_steps.html', {'form': form})
