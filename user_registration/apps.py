from django.apps import AppConfig


class UserRegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_registration'
    def ready(self):
        from .scheduler import start
        start()