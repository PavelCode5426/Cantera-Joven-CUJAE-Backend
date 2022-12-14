from django.db import models

from custom.authentication import models as authModels
from . import modelosSimple as simpleModels


class SolicitudTutorExterno(models.Model):
    area = models.ForeignKey(simpleModels.Area, on_delete=models.RESTRICT)
    joven = models.ForeignKey(authModels.DirectoryUser, on_delete=models.RESTRICT, related_name='solicitudes')
    motivo_solicitud = models.TextField()
    respuesta = models.BooleanField(null=True)
    motivo_respuesta = models.TextField(blank=True, null=True)
    fechaCreado = models.DateTimeField(auto_now=True)
    fechaRespuesta = models.DateTimeField(null=True, blank=True, default=None)


class TutoresAsignados(models.Model):
    joven = models.ForeignKey(authModels.DirectoryUser, related_name='tutores', on_delete=models.RESTRICT)
    tutor = models.ForeignKey(authModels.DirectoryUser, related_name='tutorados', on_delete=models.RESTRICT)

    fechaAsignado = models.DateTimeField(auto_now=True)
    fechaRevocado = models.DateTimeField(null=True, blank=True, default=None)
