from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the trajectories index.")

def create_trajectory(request):
    return HttpResponse("Create a trajectory when the user wants to improve a certain metric")

def update_trajectory(request):
    return HttpResponse("Based on how analytics change the trajectory will also be updated")