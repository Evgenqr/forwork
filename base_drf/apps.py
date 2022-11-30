from django.apps import AppConfig


class BaseDrfConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_drf'
