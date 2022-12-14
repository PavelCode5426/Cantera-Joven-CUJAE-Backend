from django.db import models

from core.base.models.modelosSimple import LugarProcedencia
from custom.authentication.models import DirectoryUser


class PosibleGraduado(DirectoryUser):
    lugar_pocedencia = models.ForeignKey(LugarProcedencia, models.CASCADE, editable=False,
                                         related_name='lugarPocedencia')
