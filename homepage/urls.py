from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.homepage, name="index"),
    path("log-weight/", views.log_weight, name="log_weight"),
    path("log-steps/", views.log_steps, name="log_steps"),
]
