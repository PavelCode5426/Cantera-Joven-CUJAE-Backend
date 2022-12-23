from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate

# from core.base.helpers import is_database_synchronized
# from django.db import DEFAULT_DB_ALIAS
from core.base.apps import BaseConfig
from core.base.models.modelosSimple import Dimension, Area, PropuestaMovimiento
from custom.authentication.LDAP.ldap_facade import LDAPFacade


def init_database_post_migrate(sender, app_config, *args, **kwargs):
    # if is_database_synchronized(DEFAULT_DB_ALIAS):
    # All migrations have been applied.
    if isinstance(app_config, BaseConfig) and not Area.objects.exists():
        print("Preparando Base de Datos...")

        try:
            elementos = LDAPFacade().all_areas()
        except Exception as e:
            print(e)
            elementos = [
                {
                    "name": 'Facultad de Arquitectura',
                    "distinguishedName": 'OU=Facultad de Arquitectura,DC=cujae,DC=edu,DC=cu'
                },
                {
                    "name": 'Facultad de Ingenieria Civil',
                    "distinguishedName": 'OU=Facultad de Ingenieria Civil,DC=cujae,DC=edu,DC=cu'
                },
                {
                    "name": 'Facultad de Ingenieria Electrica',
                    "distinguishedName": 'OU=Facultad de Ingenieria Electrica,DC=cujae,DC=edu,DC=cu'
                },
                {
                    "name": 'Facultad de Ingenieria Informatica',
                    "distinguishedName": 'OU=Facultad de Ingenieria Informatica,DC=cujae,DC=edu,DC=cu'
                },
            ]

        for area in elementos:
            area = dict(nombre=area['name'], distinguishedName=area['distinguishedName'])
            Area.objects.get_or_create(area, **area)

        elementos = [
            {'nombre': 'Dimension Politica Ideologica'},
        ]
        for dimension in elementos:
            Dimension.objects.get_or_create(dimension, **dimension)

        elementos = [
            {'nombre': 'Prorroga'},
            {'nombre': 'Mantener en la Cantera'},
            {'nombre': 'Alta'},
            {'nombre': 'Baja'},
        ]
        for propuesta_movimiento in elementos:
            PropuestaMovimiento.objects.get_or_create(propuesta_movimiento, **propuesta_movimiento)

        elementos = [
            {'name': 'VICERRECTOR'},
            {'name': 'JEFE DE AREA'},
            {'name': 'DIRECTOR DE RECURSOS HUMANOS'},
            {'name': 'TUTOR'},
            {'name': 'GRADUADO'},
            {'name': 'POSIBLE GRADUADO'},
            {'name': 'ESTUDIANTE'},
        ]

        for role in elementos:
            Group.objects.get_or_create(role, **role)


post_migrate.connect(init_database_post_migrate, dispatch_uid='init_database_post_migrate')
