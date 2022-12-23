from django.apps import AppConfig


class AppConfigToolkit:

    def ready(self):
        from django.apps import apps
        self.connect_signals()

        if apps.is_installed('django_q'):
            self.schedule_async_task()

        if apps.is_installed('core.configuracion'):
            self.create_configuration_variables()

    def connect_signals(self):
        pass

    def schedule_async_task(self):
        pass

    def create_configuration_variables(self):
        pass


class BaseConfig(AppConfigToolkit, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.base'

    def __init__(self, app_name, app_module):
        super(BaseConfig, self).__init__(app_name, app_module)
        self.models_module = '/models'

    def ready(self):
        from .trackers import registerModels
        registerModels()

        super(BaseConfig, self).ready()

    def connect_signals(self):
        import glob
        import importlib

        prefix = '**/receivers.py'
        files = glob.iglob(prefix, recursive=True)
        for file in files:
            file = file.replace('\\', '.') \
                .replace('.py', '') \
                .replace('/', '.')
            importlib.import_module(file)
