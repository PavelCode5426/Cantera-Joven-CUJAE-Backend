from django.db import models
from . import modelosAbstractos as abstractModels

#TODO BUSCAR LA MANERA DE CREAR NUEVO LOGHANDLER Y ESCRIBIR AQUI
# DEFINIR LOS TIPOS DE REGISTROS PROXIMAMENTE
tiposRegistros = [
    ('A','Ejemplo A'),
]
class Registro(abstractModels.AbtractUserForeignKey):
    accion = models.CharField(max_length=255,choices=tiposRegistros)
    fechaCreado = models.DateTimeField(auto_now=True)

class Alertas(abstractModels.AbtractUserForeignKey):
    texto = models.CharField(max_length=255)

class Area(abstractModels.AbstractNameEntity):
    pass

class LugarProcedencia(abstractModels.AbstractNameEntity):
    pass

class PropuestaMovimiento(abstractModels.AbstractNameEntity):
    pass

class Dimension(abstractModels.AbstractNameEntity):
    pass

class Configuracion(models.Model):
    llave = models.CharField(max_length=50,unique=True)
    valor = models.JSONField()