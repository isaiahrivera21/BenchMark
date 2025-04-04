from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the analytics index.")

def update_analytic(request):
    return HttpResponse("Should update the analytic")

def create_metric(request):
    return HttpResponse("Should create a metric that you want to keep a history of")