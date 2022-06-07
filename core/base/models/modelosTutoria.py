from django.db import models
from custom.authentication import models as authModels
from . import modelosSimple as simpleModels
from . import modelosUsuario as userModels


class SolicitudTutorExterno(models.Model):
    area = models.ForeignKey(simpleModels.Area,on_delete=models.RESTRICT)
    graduado = models.ForeignKey(userModels.Graduado,on_delete=models.RESTRICT,related_name='solicitudes')
    respuesta = models.BooleanField(null=True)
    fechaCreado = models.DateTimeField(auto_now=True)
    fechaRespuesta = models.DateTimeField(null=True,blank=True,default=None)

class GraduadoTutor(models.Model):
    graduado = models.ForeignKey(userModels.Graduado,related_name='tutores',on_delete=models.RESTRICT)
    tutor = models.ForeignKey(authModels.DirectoryUser,related_name='graduados',on_delete=models.RESTRICT)

    fechaAsignado = models.DateTimeField(auto_now=True)
    fechaRevocado = models.DateTimeField(null=True,blank=True,default=None)