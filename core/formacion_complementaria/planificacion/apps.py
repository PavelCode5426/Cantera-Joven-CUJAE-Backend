from django.apps import AppConfig


class PlanificacionFormacionComplementariaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_complementaria.planificacion'

    def ready(self):
        from core.configuracion.helpers import configValue, create_update_configuration
        from core.base.models.modelosSimple import Configuracion

        try:
            configValue('etapas_plan_formacion_complementaria')
        except Configuracion.DoesNotExist:
            create_update_configuration('etapas_plan_formacion_complementaria', 4)
            print("Create configuration vars")
        except Exception:
            pass
