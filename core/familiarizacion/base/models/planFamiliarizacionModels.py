from core.base.models import Area, Plan,  Confeccion, Actividad
from custom.authentication.models import DirectoryUser
from django.db import models

class PlanFamiliarizacion(Plan):
    anno = models.IntegerField(Default=0)

class ActividadPlanFam(Actividad):
    tipo_actividad = models.TextField()
   
    plan_familiarizacion = models.ForeignKey(PlanFamiliarizacion)
    area = models.ForeingKey(Area,models.PROTECT)


class ConfeccionPlanFamiliarizacion(Confeccion):
    plan_familiarizacion = models.ForeignKey(PlanFamiliarizacion,models.PROTECT)

