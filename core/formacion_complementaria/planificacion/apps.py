from django.apps import AppConfig


class PlanificacionFormacionComplementariaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_complementaria.planificacion'

    def ready(self):
        from core.configuracion.helpers import create_update_configuration, config
        from core.configuracion.proxy import VariableNotFoundException
        from django.conf import settings

        try:
            config('etapas_plan_formacion_complementaria')
            config('comenzar_formacion_complementaria')

            if not hasattr(settings, 'MEDIA_ROOT'):
                raise Exception('MEDIA_ROOT no configurado')

            if not hasattr(settings, 'PFC_UPLOAD_ROOT'):
                setattr(settings, 'PFC_UPLOAD_ROOT', settings.MEDIA_ROOT + '/pf-comp')

        except VariableNotFoundException:
            create_update_configuration('etapas_plan_formacion_complementaria', 4)
            create_update_configuration('comenzar_formacion_complementaria', True)
