from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.base'

    # Cargar los modelos
    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.models_module = '/models'

    def ready(self):
        self.instanceObservers()
        from .trackers import registerModels
        registerModels()

    def instanceObservers(self):
        import glob
        import importlib

        prefix = '**/receivers.py'
        files = glob.iglob(prefix, recursive=True)
        for file in files:
            file = file.replace('\\', '.') \
                .replace('.py', '') \
                .replace('/', '.')
            importlib.import_module(file)
