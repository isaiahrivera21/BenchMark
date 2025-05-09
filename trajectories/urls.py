from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_trajectory, name="create_trajectory"),
    path("update", views.update_trajectory, name="updateee_trajectory"),
    path(
        "trajectory-chart/<int:trajectory_id>/",
        views.trajectory_chart,
        name="trajectory_chart",
    ),
]
