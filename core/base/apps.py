from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.base'

    #Cargar los modelos
    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.models_module = '/models'

