from django.apps import AppConfig


class PlanificacionFormacionColectivaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_colectiva.planificacion_'

    def ready(self):
        from core.configuracion.helpers import create_update_configuration, config
        from core.configuracion.proxy import VariableNotFoundException
        from django.conf import settings

        try:
            config('etapas_plan_formacion_colectiva')
            config('comenzar_formacion_colectiva')
            config('planificar_formacion_colectiva')

            if not hasattr(settings, 'MEDIA_ROOT'):
                raise Exception('MEDIA_ROOT no configurado')

            if not hasattr(settings, 'PFC_UPLOAD_ROOT'):
                raise Exception('PFC_UPLOAD_ROOT no configurado')

        except VariableNotFoundException:
            create_update_configuration('etapas_plan_formacion_colectiva', 1)
            create_update_configuration('comenzar_formacion_colectiva', False)
            create_update_configuration('planificar_formacion_colectiva', False)
        except Exception as e:
            print(e)
