from django.apps import AppConfig


class BaseFormacionComplementariaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.formacion_individual.base'
    label = 'base_formacion_complementaria'

    def ready(self):
        from django_q.tasks import Schedule, schedule
        try:
            Schedule.objects.filter(name='autoimportarGraduados').delete()
            schedule(self.name + '.tasks.importar_graduados_automaticamente',
                     schedule_type=Schedule.CRON,
                     name='autoimportarGraduados',
                     # cron='0 0 4 * * *' #4:00 am
                     cron=' * * * * *'
                     )
            Schedule.objects.filter(name='autoimportarEstudiantes').delete()
            schedule(self.name + '.tasks.importar_estudiantes_automaticamente',
                     schedule_type=Schedule.CRON,
                     name='autoimportarEstudiantes',
                     # cron='0 0 4 * * *' #4:00 am
                     cron=' * * * * *'
                     )
        except Exception as e:
            pass
