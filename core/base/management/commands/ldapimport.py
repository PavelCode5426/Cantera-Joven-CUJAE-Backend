from django.core.management.base import BaseCommand

from core.base.models.modelosSimple import Area
from custom.authentication.LDAP.ldap_facade import LDAPFacade


class Command(BaseCommand):
    help = 'Carga todos los cuadros del directorio'

    def handle(self, *args, **options):
        areas = LDAPFacade().all_areas()
        for area in areas:
            area = dict(nombre=area['name'], distinguishedName=area['distinguishedName'])
            Area.objects.get_or_create(area, **area)

        self.stdout.write(self.style.SUCCESS('Areas del Directorio cargadas correctamente'))

        personas = LDAPFacade().all_persons_with_filter()
        for persona in personas:
            LDAPFacade().update_or_insert_user(persona)

        self.stdout.write(self.style.SUCCESS('Usuarios del directorio cargados correctamente'))
