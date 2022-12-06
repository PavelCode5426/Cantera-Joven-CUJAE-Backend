from django.contrib.auth.models import Group

from core.base.models import modelosSimple
from custom.authentication.LDAP.sigenu_ldap import SIGENU_LDAP

elementos = []
try:
    elementos = SIGENU_LDAP().areas()
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
    modelosSimple.Area.objects.get_or_create(area, **area)

elementos = [
    {'nombre': 'Dimension Politica Ideologica'},
    {'nombre': 'Dimension Prueba 1'},
    {'nombre': 'Dimension Prueba 2'},
]
for dimension in elementos:
    modelosSimple.Dimension.objects.get_or_create(dimension, **dimension)

configuracion = [
    {'etiqueta': 'auto_importar_estudiante', 'valor': False},
    {'etiqueta': 'auto_importar_posible_graduado', 'valor': True},
    {'etiqueta': 'auto_importar_graduado', 'valor': True},
    {'etiqueta': 'auto_actualizar_usuario', 'valor': True},
    {'etiqueta': 'enviar_estado_notificaciones', 'valor': True},
    {'etiqueta': 'enviar_estado_notificaciones', 'valor': True},
    {'etiqueta': 'etapas_plan_formacion_complementaria', 'valor': 4},
]

for config in configuracion:
    create, element = modelosSimple.Configuracion.objects.get_or_create(defaults=config, etiqueta=config['etiqueta'])
    if not create:
        element.update(**config)

roles = [
    {'name': 'JEFE DE AREA'},
    {'name': 'DIRECTOR DE RECURSOS HUMANOS'},
    {'name': 'ESPECIALISTA DE RECURSOS HUMANOS'},
    {'name': 'TUTOR'},
    {'name': 'ESTUDIANTE'},
    {'name': 'POSIBLE GRADUADO'},
    {'name': 'GRADUADO'},
]

for role in roles:
    Group.objects.get_or_create(role, **role)
