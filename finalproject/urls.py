"""
URL configuration for finalproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import include, path
from user import views as user_views
from homepage import views as homepage_views
from analytics import views as analytics_views
from exerciselogging import views as exercise_views
from foodlogging import views as food_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("analytics/", include("analytics.urls")),
    path("exerciselogging/", include("exerciselogging.urls")),
    path("foodlogging/", include("foodlogging.urls")),
    path("macrosAI/", include("macrosAI.urls")),
    path("trajectories/", include("trajectories.urls")),
    path("user/", include("user.urls")),
    path("", RedirectView.as_view(url="/create-user/", permanent=True)),
    path("create-user/", user_views.create_user, name="create_user"),
    path("homepage/", include("homepage.urls"), name="homepage"),
    path("log_exercise/", exercise_views.log_exercise, name="log_exercise"),
    path("exercise/", exercise_views.exercise_homepage, name="exercise_homepage"),
    path("food/", food_views.food_homepage, name="food_homepage"),
    path("log_food/", food_views.log_food, name="log_food"),
]
