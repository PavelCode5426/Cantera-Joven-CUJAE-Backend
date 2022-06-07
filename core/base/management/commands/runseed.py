from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Iniciarliza la base de datos con filas de prueba'


    def add_arguments(self, parser):
        parser.add_argument('--reset',action='store_true',default=False,help='Vacia la base de datos antes de correr los seeds')
        parser.add_argument('--check',action='store_true',default=False,help='Comprueba si hay migraciones antes de correr los seeds')
        parser.add_argument('--all',action='store_true',default=False,help='Vacia y comprueba antes de correr los seeds')


    def handle(self, *args, **options):
        if options['all'] or options['reset']:
            self.stdout.write(self.style.WARNING('Vaciando la base de datos'))
            call_command('flush',no_input=False)


        if options['all'] or options['check']:
            self.stdout.write(self.style.WARNING('Comprobando migraciones'))
            call_command('makemigrations')
            self.stdout.write(self.style.WARNING('Migrando'))
            call_command('migrate')

        self.stdout.write(self.style.WARNING('Cargando datos de prueba'))

        from core.base.seeds import execute
        execute()
        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados correctamente'))



