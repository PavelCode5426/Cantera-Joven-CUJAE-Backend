from django.db import models

from . import modelosSimple as simpleModels
from . import modelosUsuario as userModels
from .modelosPlanificacion import Actividad


class UbicacionLaboralAdelantada(models.Model):
    posiblegraduado = models.ForeignKey(userModels.PosibleGraduado, on_delete=models.RESTRICT)
    area = models.ForeignKey(simpleModels.Area, on_delete=models.RESTRICT)
    esPreubicacion = models.BooleanField(default=True)
    fechaAsignado = models.DateTimeField(auto_now=True)


class ActividadColectiva(Actividad):
    """
    LAS ACTIVIDADES QUE INTEGRARAN LA ETAPA DEL PLAN DE FAMILIARIZACION, CADA ACTIVIDAD PUEDE SER
    GENERAL (SIN AREA y esGeneral TRUE)
    GENERAL EN EL AREA => esGeneral TRUE
    ESPECIFICA EN EL SUBAREA O ESPECIFICA EN EL AREA GENERAL => esGeneral False

    LAS ACTIVIDADES GENERALES NO TENDRAN ASISTENCIA
    """
    area = models.ForeignKey(simpleModels.Area, on_delete=models.RESTRICT, default=None, null=True, blank=True)
    esGeneral = models.BooleanField(default=True)
    asistencias = models.ManyToManyField(userModels.PosibleGraduado, related_name='asistencias')
