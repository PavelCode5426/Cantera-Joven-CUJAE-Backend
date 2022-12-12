from django.db import models

from . import modelosPlanificacion as planModels
from . import modelosSimple as simpleModels
from . import modelosUsuario as userModels


class EvaluacionFinal(planModels.Evaluacion):
    propuestaMovimiento = models.ForeignKey(simpleModels.PropuestaMovimiento, on_delete=models.RESTRICT)


class EvaluacionFormacion(planModels.Evaluacion):
    replanificar = models.BooleanField(default=False)
    cerrarPlan = models.BooleanField(default=False)


class EtapaFormacion(planModels.Etapa):
    numero = models.PositiveSmallIntegerField(default=1)
    objetivo = models.CharField(max_length=255, null=True, blank=True, default=None)
    esProrroga = models.BooleanField(default=False)
    evaluacion = models.OneToOneField(EvaluacionFormacion, on_delete=models.RESTRICT, null=True, blank=True,
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


class PlanFormacion(planModels.Plan):
    evaluacion = models.OneToOneField(EvaluacionFinal, on_delete=models.RESTRICT, null=True, blank=True)

    @property
    def evaluation_approved(self):
        approved = False
        try:
            approved = self.evaluacion_id and self.evaluacion.aprobadoPor_id
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
        PENDIENTE = ('PEN', 'Pendiente de Revision')
        ESPERA = ('ESP', 'Espera de Revision')
        REVISADA = ('REV', 'Revisada')
        # CUANDO SE REPORTA PARA REVISAR Y NO SE CUMPLE SE DEJA COMO REVISADA SIEMPRE Q ESTE EN TIEMPO.
        PARCIAL = ('PAR', 'Parcialmente Cumplida')
        CUMPLIDA = ('CUM', 'Cumplida')
        INCUMPLIDA = ('INCUM', 'Incumplida')

    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDIENTE)
