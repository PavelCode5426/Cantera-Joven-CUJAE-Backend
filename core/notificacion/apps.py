from django.apps import AppConfig


class NotificacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.notificacion'
    label = 'system_notifications'

    def ready(self):
        from django_q.tasks import Schedule, schedule
        try:
            Schedule.objects.filter(name='autoEnviarEstadosNotificaciones').delete()
            schedule(self.name + '.tasks.enviar_estado_notificaciones_por_correo',
                     schedule_type=Schedule.CRON,
                     name='autoEnviarEstadosNotificaciones',
                     # cron='0 0 4 * * *' #4:00 am
                     cron=' * * * * *'
                     )
        except Exception as e:
            pass
