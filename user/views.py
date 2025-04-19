from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm  # Use default form
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # Import the new form

def index(request):
    return HttpResponse("Hello, world. You're at the user index.")

def redirect_to_create_user(request):
    return redirect('create_user')

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/create_user.html', {'form': form})

def update_user_weight(request):
    return HttpResponse("Updating user weight")

def update_user_height(request):
    return HttpResponse("Updating user height")