from custom.authentication.models import DirectoryUser
from core.base.models import LugarProcedencia
from django.db import models


class PosibleGraduado(DirectoryUser):
lugar_pocedencia = models.ForeingKey(LugarProcedencia,models.CASCADE,editable=False,related_name='lugarPocedencia')
