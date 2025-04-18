from django.apps import AppConfig


class TrajectoriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trajectories"

    def ready(self):
        # This imports your signals when the app is ready
        import trajectories.signals
