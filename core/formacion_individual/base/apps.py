from django.apps import AppConfig

from core.base.apps import AppConfigToolkit


class BaseFormacionIndividualConfig(AppConfigToolkit, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_individual.base'
    label = 'formacion_individual_base'

    def create_configuration_variables(self):
        from core.configuracion.helpers import create_update_configuration, config
        from core.configuracion.proxy import VariableNotFoundException
        from django.db import ProgrammingError

        try:
            config('mantener_actualizada_informacion_de_estudiantes')
            config('mantener_actualizada_informacion_de_graduados')
        except VariableNotFoundException:
            create_update_configuration('mantener_actualizada_informacion_de_estudiantes', True)
            create_update_configuration('mantener_actualizada_informacion_de_graduados', True)
        except ProgrammingError:
            pass
        except Exception as e:
            print(e)

    def schedule_async_task(self):
        from django_q.tasks import Schedule, schedule
        try:
            job_name = 'actualizarInformacionGraduadosJob'
            Schedule.objects.filter(name=job_name).delete()
            schedule(self.name + '.tasks.actualizar_informacion_graduados',
                     schedule_type=Schedule.CRON,
                     name=job_name,
                     cron='0 0 4 * * *'  # 4:00 am
                     # cron=' * * * * *'
                     )

            job_name = 'actualizarInformacionEstudiantesJob'
            Schedule.objects.filter(name=job_name).delete()
            schedule(self.name + '.tasks.actualizar_informacion_estudiantes',
                     schedule_type=Schedule.CRON,
                     name=job_name,
                     cron='0 0 4 * * *'  # 4:00 am
                     # cron=' * * * * *'
                     )
        except Exception as e:
            pass
