from django.apps import AppConfig

class LoggingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom.logging'

    def ready(self):
        from django.apps import apps
        if apps.is_installed('django.contrib.admin'):
            from . import signals
            from django.db.models.signals import post_delete,post_save

            post_delete.connect(signals.post_delete_action_logging)
            post_save.connect(signals.post_save_action_logging)

