from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Analytics


def index(request):
    return HttpResponse("Hello, world. You're at the analytics index.")

def metrics_display(request):
    initial_metrics = Analytics.objects.all() 
    return render(request, 'analytics/analytics_display.html',{'initial_metrics': initial_metrics})

def avg_macros_all_time_display(request):
    intial_metrics = Analytics.objects.all()
    return render(request, 'analytics/all_time_macros_display.html',{'initial_metrics': intial_metrics})

def avg_macros_weekly_display(request):
    intial_metrics = Analytics.objects.all()
    return render(request, 'analytics/weekly_macros_display.html',{'initial_metrics': intial_metrics})

def avg_macros_monthly_display(request):
    intial_metrics = Analytics.objects.all()
    return render(request, 'analytics/monthly_macros_display.html',{'initial_metrics': intial_metrics})