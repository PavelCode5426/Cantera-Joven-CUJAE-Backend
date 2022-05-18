from django.apps import AppConfig


class BaseFormacionComplementariaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_complementaria.base'
    label = 'base_formacion_complementaria'

    def __init__(self,app_name,app_module):
        super().__init__(app_name,app_module)
        self.models_module='/models'
