from django.contrib.auth.models import Group

from core.base.models import modelosSimple
from custom.authentication.LDAP.sigenu_ldap import SIGENU_LDAP

elementos = SIGENU_LDAP().areas()
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
]

for config in configuracion:
    create, element = modelosSimple.Configuracion.objects.get_or_create(defaults=config, etiqueta=config['etiqueta'])
    if not create:
        element.update(**config)

roles = [
    {'name': 'Jefe de Area'},
    {'name': 'Director de Recursos Humanos'},
    {'name': 'Tutor'},
    {'name': 'Estudiante'},
    {'name': 'Posible Graduado'},
    {'name': 'Graduado'},
]

for role in roles:
    Group.objects.get_or_create(role, **role)
