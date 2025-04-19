from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path("", views.index, name="index"),
    path("update_weight",views.update_user_weight,name="update_weight"),
    path("update_height",views.update_user_height,name="update_height"),
    path('create/', views.create_user, name='create_user'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name='logout'),
    path('', views.redirect_to_create_user), # root redirects to this 
]