from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create",views.log_exercise,name="create_exercise"),
    path("delete/<int:id>/",views.delete_exercise,name="delete_exercise"),
    path("edit/<int:id>/", views.edit_exercise, name="edit_exercise"),
    path('exercises/', views.list_all_exercise, name='list_all_exercise'),
    path('exercise_homepage/', views.exercise_homepage, name='exercise_homepage'),
    path('exercise_homepage/<str:exercise_name>/', views.exercise_detail, name='exercise_detail'),
    path('exercise-autocomplete/', views.exercise_autocomplete, name='exercise-autocomplete')
]