from django.apps import AppConfig


class PlanificacionFormacionIndividualConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_individual.planificacion'

    def ready(self):
        from core.configuracion.helpers import create_update_configuration, config
        from core.configuracion.proxy import VariableNotFoundException
        from django.conf import settings

        try:
            config('etapas_plan_formacion_individual_graduado')
            config('etapas_plan_formacion_individual_estudiante')
            config('etapas_de_prorroga_formacion_individual')
            config('comenzar_formacion_complementaria')

            if not hasattr(settings, 'MEDIA_ROOT'):
                raise Exception('MEDIA_ROOT no configurado')

            if not hasattr(settings, 'PFI_UPLOAD_ROOT'):
                raise Exception('PFI_UPLOAD_ROOT no configurado')

        except VariableNotFoundException:
            create_update_configuration('etapas_plan_formacion_individual_graduado', 4)
            create_update_configuration('etapas_plan_formacion_individual_estudiante', 2)
            create_update_configuration('comenzar_formacion_complementaria', True)
            create_update_configuration('etapas_de_prorroga_formacion_individual', 3)
        except Exception as e:
            print(e)
