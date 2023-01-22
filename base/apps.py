from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
    verbose_name = 'База знаний'

    # def ready(self):
    #     # Implicitly connect a signal handlers decorated with @receiver.
    #     from . import signals
    #  Explicitly connect a signal handler.
    #  signals.pre_save.connect(signals.test2,
    #  dispatch_uid="my_unique_identifier")
