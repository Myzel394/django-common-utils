from django.apps import AppConfig


class Config(AppConfig):
    name = "django_common_utils"
    
    def ready(self):
        from . import signals
