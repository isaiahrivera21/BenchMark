from django.contrib import admin

# Register your models here.
from .models import Trajectory
from .forms import TrajectoryForm

@admin.register(Trajectory)
class TrajectoryAdmin(admin.ModelAdmin):
    form = TrajectoryForm