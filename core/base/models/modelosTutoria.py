from django.db import models
from custom.authentication import models as authModels
from . import modelosSimple as simpleModels
from . import modelosUsuario as userModels


class SolicitudTutorExterno(models.Model):
    area = models.ForeignKey(simpleModels.Area,on_delete=models.RESTRICT)
    graduado = models.ForeignKey(userModels.Graduado,on_delete=models.RESTRICT)
    respuesta = models.BooleanField(null=True)
    fechaCreado = models.DateTimeField(auto_now=True)
    fechaRespuesta = models.DateTimeField(null=True,blank=True,default=None)

class GraduadoTutor(models.Model):
    graduado = models.ForeignKey(userModels.Graduado,related_name='tutorado',on_delete=models.RESTRICT)
    tutor = models.ForeignKey(authModels.DirectoryUser,on_delete=models.RESTRICT)

    fechaAsignado = models.DateTimeField(auto_now=True)
    fechaRevocado = models.DateTimeField(null=True,blank=True,default=None)