from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create",views.log_food,name="create_user_food"),
    path("delete/<int:id>/",views.delete_food,name="delete_food"),
    path("edit/<int:id>/", views.edit_food, name="edit_food"),
    path('foods/', views.list_all_food, name='list_all_foods')
]