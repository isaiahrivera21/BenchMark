from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('metrics/', views.metrics_display, name='metrics_display'),
    path('avg_macros_all_time/', views.avg_macros_all_time_display, name='avg_macros_all_time_display'),
    path('avg_macros_weekly/', views.avg_macros_weekly_display, name='avg_macros_weekly_display'),
    path('avg_macros_monthly/', views.avg_macros_monthly_display, name='avg_macros_monthly_display')
]
