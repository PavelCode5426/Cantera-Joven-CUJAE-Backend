from django.apps import AppConfig

from core.base.apps import AppConfigToolkit


class FormacionColectivaConfig(AppConfigToolkit, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_colectiva.base'
    label = 'formacion_colectiva_base'

    def schedule_async_task(self):
        from django_q.tasks import Schedule, schedule
        try:
            job_name = 'actualizarInformacionPosiblesGraduadosJob'
            Schedule.objects.filter(name=job_name).delete()
            schedule(self.name + '.tasks.actualizar_informacion_posibles_graduados',
                     schedule_type=Schedule.CRON,
                     name=job_name,
                     # cron='0 0 4 * * *' #4:00 am
                     cron=' * * * * *'
                     )
        except Exception as e:
            pass

    def create_configuration_variables(self):
        from core.configuracion.helpers import create_update_configuration, config
        from core.configuracion.proxy import VariableNotFoundException
        from django.db import ProgrammingError

        try:
            config('mantener_actualizada_informacion_de_posibles_graduados')
        except VariableNotFoundException:
            create_update_configuration('mantener_actualizada_informacion_de_posibles_graduados', True)
        except ProgrammingError:
            pass
        except Exception as e:
            print(e)
