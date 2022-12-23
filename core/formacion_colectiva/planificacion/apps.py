from core.base.apps import AppConfigToolkit, AppConfig


class PlanificacionFormacionColectivaConfig(AppConfigToolkit, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_colectiva.planificacion'
    label = 'formacion_colectiva_planificacion'

    def create_configuration_variables(self):
        from core.configuracion.helpers import create_update_configuration, config
        from core.configuracion.proxy import VariableNotFoundException
        from django.db import ProgrammingError
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
        except ProgrammingError:
            pass
        except Exception as e:
            print(e)
