from django.apps import AppConfig

from core.base.apps import AppConfigToolkit


class AuthConfig(AppConfigToolkit, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom.authentication'

    def create_configuration_variables(self):
        from core.configuracion.helpers import create_update_configuration, config
        from core.configuracion.proxy import VariableNotFoundException
        from django.db import ProgrammingError

        try:
            config('mantener_actualizada_informacion_de_usuarios')
        except VariableNotFoundException:
            create_update_configuration('mantener_actualizada_informacion_de_usuarios', True)
        except ProgrammingError:
            pass
        except Exception as e:
            print(e)

    def schedule_async_task(self):
        from django_q.tasks import schedule, Schedule
        try:
            job_name = 'actualizarInformacionUsuariosJob'
            Schedule.objects.filter(name=job_name).delete()
            schedule(self.name + '.tasks.actualizar_informacion_usuarios',
                     schedule_type=Schedule.CRON,
                     name=job_name,
                     # cron='0 0 5 * * *' #5:00 am
                     cron=' * * * * *'
                     )
        except Exception as e:
            pass
