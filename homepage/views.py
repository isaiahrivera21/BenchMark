from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm  # Use default form
from django.contrib.auth import login

# so we want to render a form that just has two buttons that take you to one link or the other resectivly. Then probably in a header 1 something like this is the homepage. 
def homepage(request):
    return render(request, 'homepage/index.html')
    
