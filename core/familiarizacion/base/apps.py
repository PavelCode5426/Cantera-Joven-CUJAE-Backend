from django.apps import AppConfig


class FamiliarizacionBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.familiarizacion.base'
    label = 'base_familiarizacion'

    def ready(self):
        from django_q.tasks import Schedule, schedule
        try:
            Schedule.objects.filter(name='autoimportarPosiblesGraduados').delete()
            schedule(self.name+'.tasks.importar_posibles_graduados_automaticamente',
                     schedule_type=Schedule.CRON,
                     name='autoimportarPosiblesGraduados',
                     # cron='0 0 4 * * *' #4:00 am
                     cron=' * * * * *'
                     )
        except Exception as e:
            pass

