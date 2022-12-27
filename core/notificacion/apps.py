from django.apps import AppConfig

from core.base.apps import AppConfigToolkit


class NotificacionConfig(AppConfigToolkit, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.notificacion'

    def create_configuration_variables(self):
        from core.configuracion.helpers import create_update_configuration, config
        from core.configuracion.proxy import VariableNotFoundException
        from django.db import ProgrammingError

        try:
            config('enviar_notificaciones_por_correo')
        except VariableNotFoundException:
            create_update_configuration('enviar_notificaciones_por_correo', True)
        except ProgrammingError as e:
            pass
        except Exception as e:
            print(e)

    def schedule_async_task(self):
        from django_q.tasks import Schedule, schedule
        try:
            Schedule.objects.filter(name='enviarNotificacionesPorCorreoJob').delete()
            schedule(self.name + '.tasks.enviar_notificaciones_por_correo',
                     schedule_type=Schedule.CRON,
                     name='enviarNotificacionesPorCorreoJob',
                     cron='0 0 4 * * *')  # 4:00 am
            # cron=' * * * * *')
        except Exception as e:
            pass
