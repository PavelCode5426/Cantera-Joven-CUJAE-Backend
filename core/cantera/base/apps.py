from django.apps import AppConfig


class CanteraBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.cantera.base'
    label = 'base_cantera'

    def ready(self):
        from django_q.tasks import Schedule, schedule
        try:
            Schedule.objects.filter(name='autoimportarEstudiantes').delete()
            schedule(self.name+'.tasks.importar_estudiantes_automaticamente',
                     schedule_type=Schedule.CRON,
                     name='autoimportarEstudiantes',
                     # cron='0 0 4 * * *' #4:00 am
                     cron=' * * * * *'
                     )
        except Exception as e:
            pass


