from django.apps import AppConfig


class FamiliarizacionBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.familiarizacion.base'
    label = 'base_familiarizacion'

    def __init__(self,app_name,app_module):
        super().__init__(app_name,app_module)
        self.models_module='/models'
