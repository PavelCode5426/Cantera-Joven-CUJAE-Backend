from django.apps import AppConfig

class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom.authentication'

    def ready(self):
        from django.apps import apps

        if apps.is_installed('django_q'):
            from django_q.tasks import schedule,Schedule

            try:
                Schedule.objects.filter(name='actualizarInformacionUsuarios').delete()
                schedule(self.name+'.tasks.actualizar_informacion_usuarios',
                         schedule_type=Schedule.CRON,
                         name='actualizarInformacionUsuarios',
                         #cron='0 0 5 * * *' #5:00 am
                         cron=' * * * * *'
                         )
            except Exception as e:
                pass