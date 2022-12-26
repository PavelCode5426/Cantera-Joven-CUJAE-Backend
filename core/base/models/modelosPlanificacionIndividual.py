from django.db import models

from custom.authentication import models as authModels
from custom.authentication.models import DirectoryUser
from . import modelosSimple as simpleModels
from .modelosPlanificacion import Plan, Etapa, Evaluacion, Actividad


class SolicitudTutorExterno(models.Model):
    area = models.ForeignKey(simpleModels.Area, on_delete=models.RESTRICT)
    joven = models.ForeignKey(authModels.DirectoryUser, on_delete=models.RESTRICT, related_name='solicitudes')
    motivo_solicitud = models.TextField()
    respuesta = models.BooleanField(null=True)
    motivo_respuesta = models.TextField(blank=True, null=True)
    fechaCreado = models.DateTimeField(auto_now=True)
    fechaRespuesta = models.DateTimeField(null=True, blank=True, default=None)


class TutoresAsignados(models.Model):
    joven = models.ForeignKey(authModels.DirectoryUser, related_name='tutores', on_delete=models.RESTRICT)
    tutor = models.ForeignKey(authModels.DirectoryUser, related_name='tutorados', on_delete=models.RESTRICT)

    fechaAsignado = models.DateTimeField(auto_now=True)
    fechaRevocado = models.DateTimeField(null=True, blank=True, default=None)


class EvaluacionFinal(Evaluacion):
    propuestaMovimiento = models.ForeignKey(simpleModels.PropuestaMovimiento, on_delete=models.RESTRICT)


class EvaluacionFormacion(Evaluacion):
    replanificar = models.BooleanField(default=False)
    cerrarPlan = models.BooleanField(default=False)


class EtapaFormacion(Etapa):
    numero = models.PositiveSmallIntegerField(default=1)
    objetivo = models.CharField(max_length=255, null=True, blank=True, default=None)
    esProrroga = models.BooleanField(default=False)
    evaluacion = models.OneToOneField(EvaluacionFormacion, on_delete=models.RESTRICT, null=True, blank=True,
                                      default=None)

    @property
    def graduado(self):
        return PlanFormacion.objects.get(pk=self.plan).usuario

    @property
    def estudiante(self):
        return PlanFormacion.objects.get(pk=self.plan).usuario

    @property
    def evaluation_approved(self):
        approved = False
        try:
            approved = self.evaluacion and self.evaluacion.aprobadoPor
        except Exception:
            pass

        return approved


class PlanFormacion(Plan):
    joven = models.ForeignKey(DirectoryUser, related_name='planesformacion', on_delete=models.RESTRICT)
    evaluacion = models.OneToOneField(EvaluacionFinal, on_delete=models.RESTRICT, null=True, blank=True)
    evaluacion_prorroga = models.OneToOneField(EvaluacionFinal, on_delete=models.RESTRICT, null=True, blank=True)

    @property
    def evaluation_approved(self):
        approved = False
        try:
            approved = self.evaluacion_id and self.evaluacion.aprobadoPor_id
        except Exception:
            pass

        return approved

    @property
    def evaluation_prorroga_approved(self):
        approved = False
        try:
            approved = self.evaluacion_prorroga_id and self.evaluacion_prorroga.aprobadoPor_id
        except Exception:
            pass

        return approved


class ActividadFormacion(Actividad):
    fechaCumplimiento = models.DateTimeField(null=True, blank=True, default=None)

    class Estado(models.TextChoices):
        PENDIENTE = 'Pendiente'
        ESPERA = 'Espera de Revision'
        REVISADA = 'Revisada'
        # CUANDO SE REPORTA PARA REVISAR Y NO SE CUMPLE SE DEJA COMO REVISADA SIEMPRE Q ESTE EN TIEMPO.
        PARCIAL = 'Parcialmente Cumplida'
        CUMPLIDA = 'Cumplida'
        INCUMPLIDA = 'Incumplida'

    estado = models.CharField(max_length=25, choices=Estado.choices, default=Estado.PENDIENTE)
