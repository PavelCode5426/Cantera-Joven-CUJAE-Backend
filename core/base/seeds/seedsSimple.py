from django.contrib.auth.models import Group

from core.base.models import modelosSimple

elementos = [
    {'nombre': 'Informatica'},
    {'nombre': 'Civil'},
    {'nombre': 'Industrial'},
    {'nombre': 'Vicerectoria'},
    {'nombre': 'Decanato'},
    {'nombre': 'Recursos Humanos'},
    {'nombre': 'Quimica'},
    {'nombre': 'Electrica'},
    {'nombre': 'Mantenimiento'},
]
for area in elementos:
    modelosSimple.Area.objects.get_or_create(area, **area)

elementos = [
    {'nombre': 'Universidad de la Habana'},
    {'nombre': 'Universidad de Ciencias Informaticas'},
    {'nombre': 'Universidad Tecnologica de la Habana'},
    {'nombre': 'Universidad Pedagogica de la Habana'},
]
for lugar_procedencia in elementos:
    modelosSimple.LugarProcedencia.objects.get_or_create(lugar_procedencia, **lugar_procedencia)

elementos = [
    {'nombre': 'Dimension Politica Ideologica'},
    {'nombre': 'Dimension Prueba 1'},
    {'nombre': 'Dimension Prueba 2'},
]
for dimension in elementos:
    modelosSimple.Dimension.objects.get_or_create(dimension, **dimension)

configuracion = [
    {'llave': 'auto_importar_estudiante', 'valor': True},
    {'llave': 'auto_importar_posible_graduado', 'valor': True},
    {'llave': 'auto_importar_graduado', 'valor': True},
    {'llave': 'auto_actualizar_usuario', 'valor': True},
    {'llave': 'enviar_estado_notificaciones', 'valor': True},
]

for config in configuracion:
    modelosSimple.Configuracion.objects.update_or_create(llave=config['llave'], defaults=config)

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
