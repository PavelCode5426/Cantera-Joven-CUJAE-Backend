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

