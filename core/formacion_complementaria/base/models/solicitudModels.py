from django.db import models
from core.base.models import Area, ActividadCanteraFormacionComplementaria


class Solicitud(models.Model):
    respuesta = models.BooleanField(default=None,null=True,blank=True)
    fecha_solicitud = models.DateTimeField(auto_now=True,editable=False)
    fecha_respuesta = models.DateTimeField(default=None,null=True,blank=True)

class SolicitudTutor(Solicitud):
    area = models.ForeignKey(Area,models.CASCADE)

class SolicitudMovimiento(Solicitud):
    baja = models.BooleanField(default=None,null=True,blank=True)

class SolicitudRevisionTarea(Solicitud):
    tarea = models.ForeignKey(ActividadCanteraFormacionComplementaria,models.CASCADE)