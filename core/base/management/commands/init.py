from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Iniciarliza la base de datos con filas de prueba'

    def add_arguments(self, parser):
        parser.add_argument('--seed', action='store_true', default=False, help='Inicializa con datos de prueba')

    def handle(self, *args, **options):
        if options['seed']:
            call_command('runseed')
        call_command('migrate')
        call_command('runserver', "0.0.0.0:8000")
