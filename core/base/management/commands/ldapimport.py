from django.core.management import call_command
from django.core.management.base import BaseCommand

from custom.authentication.LDAP.ldap_facade import LDAPFacade
from custom.authentication.LDAP.sigenu_ldap_services import SIGENU_LDAP_Services
from custom.authentication.models import DirectoryUser


class Command(BaseCommand):
    help = 'Carga todos los cuadros del directorio'


    def handle(self, *args, **options):
        personas = LDAPFacade().all_persons_with_filter()
        for persona in personas:
            #try:
            LDAPFacade().update_or_insert_user(persona)
            #except Exception:
             #   print(persona)


        self.stdout.write(self.style.SUCCESS('Usuarios del directorio cargados correctamente'))

