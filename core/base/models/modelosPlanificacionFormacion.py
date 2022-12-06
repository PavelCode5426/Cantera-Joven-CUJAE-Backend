from django.db import models

from . import modelosPlanificacion as planModels
from . import modelosSimple as simpleModels
from . import modelosUsuario as userModels


class EtapaFormacion(planModels.Etapa):
    numero = models.PositiveSmallIntegerField(default=1)
    objetivo = models.CharField(max_length=255, null=True, blank=True, default=None)
    esProrroga = models.BooleanField(default=False)
    evaluacion = models.OneToOneField(planModels.Evaluacion, on_delete=models.RESTRICT, null=True, blank=True,
                                      default=None)

    @property
    def graduado(self):
        return PlanFormacionComplementaria.objects.get(pk=self.plan).graduado

    @property
    def estudiante(self):
        return PlanFormacionCantera.objects.get(pk=self.plan).estudiante

    @property
    def evaluation_approved(self):
        approved = False
        try:
            approved = self.evaluacion and self.evaluacion.aprobadoPor
        except Exception:
            pass

        return approved


class EvaluacionFinal(planModels.Evaluacion):
    propuestaMovimiento = models.ForeignKey(simpleModels.PropuestaMovimiento, on_delete=models.RESTRICT)


class PlanFormacion(planModels.Plan):
    evaluacion = models.OneToOneField(EvaluacionFinal, on_delete=models.RESTRICT, null=True, blank=True)

    @property
    def evaluation_approved(self):
        approved = False
        try:
            approved = self.evaluacion and self.evaluacion.aprobadoPor
        except Exception:
            pass

        return approved


class PlanFormacionCantera(PlanFormacion):
    estudiante = models.OneToOneField(userModels.Estudiante, on_delete=models.RESTRICT)


class PlanFormacionComplementaria(PlanFormacion):
    graduado = models.OneToOneField(userModels.Graduado, on_delete=models.RESTRICT)


class ActividadFormacion(planModels.Actividad):
    fechaCumplimiento = models.DateTimeField(null=True, blank=True, default=None)
    fechaFin = models.DateTimeField()

    class Estado(models.TextChoices):
        PENDIENTE = 'Pendiente'
        ESPERA = 'Espera de Revision'
        REVISADA = 'Revisada'  # CUANDO SE REPORTA PARA REVISAR Y NO SE CUMPLE SE DEJA COMO REVISADA SIEMPRE Q ESTE EN TIEMPO.
        PARCIAL = 'Parcialmente Cumplida'
        CUMPLIDA = 'Cumplida'
        INCUMPLIDA = 'Incumplida'

    estadoActividad = models.CharField(max_length=50, choices=Estado.choices, default=Estado.PENDIENTE)
