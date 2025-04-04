from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create",views.log_exercise,name="create_exercise"),
    path("delete/<int:id>/",views.delete_exercise,name="delete_exercise"),
    path("edit/<int:id>/", views.edit_exercise, name="edit_exercise"),
    path('exercises/', views.list_all_exercise, name='list_all_exercise')
]