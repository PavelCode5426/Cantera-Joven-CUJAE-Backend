from core.base.models import modelosSimple

elementos = [
    {'nombre':'Informatica'},
    {'nombre':'Civil'},
    {'nombre':'Industrial'},
    {'nombre':'Vicerectoria'},
    {'nombre':'Decanato'},
    {'nombre':'Recursos Humanos'},
    {'nombre':'Quimica'},
    {'nombre':'Electrica'},
    {'nombre':'Mantenimiento'},
]
for area in elementos:
    modelosSimple.Area.objects.create(**area)

elementos = [
    {'nombre':'Universidad de la Habana'},
    {'nombre':'Universidad de Ciencias Informaticas'},
    {'nombre':'Universidad Tecnologica de la Habana'},
    {'nombre':'Universidad Pedagogica de la Habana'},
]
for lugar_procedencia in elementos:
    modelosSimple.LugarProcedencia.objects.create(**lugar_procedencia)

elementos = [
    {'nombre': 'Dimension Politica Ideologica'},
    {'nombre': 'Dimension Prueba 1'},
    {'nombre': 'Dimension Prueba 2'},
]
for dimension in elementos:
    modelosSimple.Dimension.objects.create(**dimension)

configuracion = [
    {'llave':'auto_importar_estudiante','valor':True},
    {'llave':'auto_importar_posible_graduado','valor':True},
    {'llave':'auto_importar_graduado','valor':True},
    {'llave':'auto_actualizar_usuario','valor':True},
    {'llave':'enviar_estado_notificaciones','valor':True},
]

for config in configuracion:
    modelosSimple.Configuracion.objects.update_or_create(llave=config['llave'],defaults=config)

from django.contrib.auth.models import Group

roles = [
    {'nombre':'Tutor'},
    {'nombre':'Jefe de Area'},
    {'nombre':'Director Recursos Humanos'},
    {'nombre':'Vicerrector'},
    {'nombre':'Estudiante'},
    {'nombre':'Graduado'},
    {'nombre':'Posible Graduado'},
]
for Group in roles:
    Group.objects.update_or_create()