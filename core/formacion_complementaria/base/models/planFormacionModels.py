from core.base.models import Etapa, Plan, Evaluacion, Confeccion, Actividad
from core.formacion_complementaria.base.models import Graduado
from custom.authentication.models import DirectoryUser
from django.db import models


class PlanFormacionComplementaria(Plan):
    firmado_por_graduado = models.BooleanField(default=False)

    graduado = models.ForeignKey(Graduado,models.PROTECT)
    aprobado_por = models.ForeignKey(DirectoryUser,models.PROTECT)
    evaluacion = models.ForeignKey(Evaluacion,models.PROTECT,default=None,null=True,blank=True)

class EtapaFormacionComplementaria(Etapa):
    plan_formacion_complementaria = models.ForeignKey(PlanFormacionComplementaria)

class ConfeccionPlanFormacionComplementaria(Confeccion):
    plan_formacion_complementaria = models.ForeignKey(PlanFormacionComplementaria,models.PROTECT)



