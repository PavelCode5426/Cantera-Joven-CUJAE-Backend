from core.base.apps import AppConfigToolkit, AppConfig


class PlanificacionFormacionIndividualConfig(AppConfigToolkit, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_individual.planificacion'
    label = 'formacion_individual_planificacion'

    def create_configuration_variables(self):
        from core.configuracion.helpers import create_update_configuration, config
        from core.configuracion.proxy import VariableNotFoundException
        from django.db import ProgrammingError

        from django.conf import settings

        try:
            config('etapas_plan_formacion_individual_graduado')
            config('etapas_plan_formacion_individual_estudiante')
            config('etapas_de_prorroga_formacion_individual')
            config('comenzar_formacion_individual')

            if not hasattr(settings, 'MEDIA_ROOT'):
                raise Exception('MEDIA_ROOT no configurado')

            if not hasattr(settings, 'PFI_UPLOAD_ROOT'):
                raise Exception('PFI_UPLOAD_ROOT no configurado')

        except VariableNotFoundException:
            create_update_configuration('etapas_plan_formacion_individual_graduado', 4)
            create_update_configuration('etapas_plan_formacion_individual_estudiante', 2)
            create_update_configuration('comenzar_formacion_individual', False)
            create_update_configuration('etapas_de_prorroga_formacion_individual', 2)
        except ProgrammingError as e:
            pass
        except Exception as e:
            print(e)
