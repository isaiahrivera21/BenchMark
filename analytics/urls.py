from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create",views.create_metric,name="create_metric"),
    path("update",views.update_analytic,name="update_analytic")
]