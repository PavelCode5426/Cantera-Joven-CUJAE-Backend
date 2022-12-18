from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Iniciarliza la base de datos con filas de prueba'

    def handle(self, *args, **options):
        call_command('migrate')
        call_command('runseed')
