from django.db import models

from custom.authentication import models as authModels
from . import modelosAbstractos as abstractModels
from . import modelosSimple as simpleModels


class Evaluacion(models.Model):
    texto = models.CharField(max_length=255)
    esSatisfactorio = models.BooleanField(default=True)
    aprobadoPor = models.ForeignKey(authModels.DirectoryUser, models.RESTRICT, null=True, blank=True)


class Plan(models.Model):
    fechaCreado = models.DateTimeField(auto_now_add=True)
    aprobadoPor = models.ForeignKey(authModels.DirectoryUser, on_delete=models.RESTRICT, blank=True, null=True)

    class Estados(models.TextChoices):
        ENDESARROLLO = ('DEV', 'En Desarrollo')
        PENDIENTE = ('PEN', 'Pendiente de Revision')
        RECHAZADO = ('REC', 'Rechazado')
        APROBADO = ('APR', 'Aprobado')

    estado = models.CharField(choices=Estados.choices, max_length=100, default=Estados.ENDESARROLLO)

    @property
    def is_approved(self):
        return self.Estados.APROBADO == self.estado


class Etapa(models.Model):
    fechaInicio = models.DateTimeField(null=True, blank=True, default=None)
    fechaFin = models.DateTimeField(null=True, blank=True, default=None)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='etapas')


class Actividad(abstractModels.AbstractNameEntity):
    descripcion = models.CharField(max_length=255)
    observaciones = models.CharField(max_length=255)
    fechaInicio = models.DateTimeField()

    dimesion = models.ForeignKey(simpleModels.Dimension, on_delete=models.RESTRICT)
    responsable = models.ForeignKey(authModels.DirectoryUser, related_name='responsable', on_delete=models.RESTRICT)
    # participantes = models.ManyToManyField(authModels.DirectoryUser, related_name='participantes')

    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE, related_name='tareas')
    actividadPadre = models.ForeignKey('Actividad', on_delete=models.RESTRICT)


class Archivo(models.Model):
    """
    LOS ARCHIVOS SON PARA GUARDAR COSAS PERTENECIENTES A LAS ACTIVIDADES O LOS PLANES
    EN CASO DE UTILIZAR EL ARCHIVO PARA EL CONTROL DE VERSIONES SE UTILIZA LA COLUMNA EN TRUE
    POR LA FECHA SE SABRA CUAL ES EL MOMENTO DE CADA VERSION
    """
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FilePathField()
    plan = models.ForeignKey(Plan, on_delete=models.RESTRICT, related_name='versiones')
    versionado = models.BooleanField(default=False)
    actividad = models.ForeignKey(Actividad, on_delete=models.RESTRICT, related_name='documentos')


class Comentario(abstractModels.AbtractUserForeignKey):
    """
    LOS COMENTARIOS PERTENECEN AL PLAN O LA ACTIVIDAD
    """
    texto = models.CharField(max_length=255)
    plan = models.ForeignKey(Plan, null=True, blank=True, default=None, on_delete=models.RESTRICT)
    actividad = models.ForeignKey(Actividad, null=True, blank=True, default=None, on_delete=models.RESTRICT)
