from core.base.models import Etapa, Plan
from core.formacion_complementaria.base.models import Estudiante
from custom.authentication.models import DirectoryUser
from django.db import models


class PlanCantera(Plan):
    estudiante = models.ForeignKey(Estudiante,models.PROTECT)    

class EtapaCantera(Etapa):
    plan_cantera = models.ForeignKey(PlanCantera)