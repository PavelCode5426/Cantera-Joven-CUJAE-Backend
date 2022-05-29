from django.db import models
from . import modelosSimple as simpleModels
from . import modelosUsuario as userModels

class UbicacionLaboralAdelantada(models.Model):
    estudiante = models.ForeignKey(userModels.PosibleGraduado,on_delete=models.RESTRICT)
    area = models.ForeignKey(simpleModels.Area,on_delete=models.RESTRICT)
    esPreubicacion = models.BooleanField(default=True)
    fechaAsignado = models.DateTimeField(auto_now=True)