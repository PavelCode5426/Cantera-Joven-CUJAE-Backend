from django.db import models

from . import modelosUsuario as userModels
from . import modelosSimple as simpleModels
from . import modelosAbstractos as abstractModels
from custom.authentication import models as authModels


class Evaluacion(models.Model):
    texto = models.CharField(max_length=255)
    esSatisfactorio = models.BooleanField(default=True)
    tipoMovimiento = models.ForeignKey(simpleModels.PropuestaMovimiento, null=True, blank=True, default=None,on_delete=models.RESTRICT)

    class NotasEvaluacion(models.TextChoices):
        MAL = 'M','Mal'
        REGULAR = 'R','Regular'
        BIEN = 'B','Bien'
        MUYBIEN = 'MB','Muy Bien'
        EXCELENTE = 'E','Excelente'
    nota = models.CharField(max_length=25,choices=NotasEvaluacion.choices,default=NotasEvaluacion.BIEN)

class Plan(models.Model):
    #Estudiante de Plan Cantera
    estudiante = models.ForeignKey(userModels.Estudiante,null=True,blank=True,default=None,on_delete=models.RESTRICT)

    #Graduado de Plan de Formacion Complementaria
    graduado = models.ForeignKey(userModels.Graduado,related_name='graduado',null=True,blank=True,default=None,on_delete=models.RESTRICT)
    firmadoPorGraduado = models.BooleanField(null=True) #Si es verdadero lo aprueba, si es falso lo rechaza.

    #Usuario que aprueba el Plan
    aprobadoPor = models.ForeignKey(authModels.DirectoryUser,related_name='aprobadoPor',null=True,blank=True,default=None,on_delete=models.RESTRICT)

    #Evaluacion Final del Graduado o Estudiante en el Plan de Formacion Cantera o Plan de Formacion Complementaria
    evaluacion = models.ForeignKey(Evaluacion,null=True,blank=True,default=None,on_delete=models.RESTRICT)

    #Refleja el estado del Plan, puede ser EN Desarrollo, PENDIENTE, RECHAZADO, APROBADO ........
    class EstadosPlan(models.TextChoices):
        ENDESARROLLO = ('DEV','En Desarrollo')
        PENDIENTE = ('PEN','Pendiente de Aprobacion')
        RECHAZADO = ('REC','Rechazado')
        APROBADO = ('APR','Aprobado')

    estado = models.CharField(max_length=50,choices=EstadosPlan.choices,default=EstadosPlan.ENDESARROLLO)
    fechaCreado = models.DateTimeField(auto_now=True)
    version = models.PositiveSmallIntegerField(default=1)

class Etapa(models.Model):
    numero = models.PositiveSmallIntegerField(default=1)

    #El objetivo de la etapa puede ser null ya que el Plan de Familiarizacion no tiene objetivos
    objetivo = models.CharField(max_length=255,null=True,blank=True,default=None)
    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()
    evaluacion = models.ForeignKey(Evaluacion,on_delete=models.RESTRICT)
    planes = models.ManyToManyField(Plan)

class Actividad(abstractModels.AbstractNameEntity):
    descripcion = models.CharField(max_length=255)
    observaciones = models.CharField(max_length=255)
    fechaInicio = models.DateTimeField()
    fechaCumplimiento = models.DateTimeField(null=True,blank=True,default=None) #Para el adiestramiento y cantera
    fechaFin = models.DateTimeField()

    class EstadoActividad(models.TextChoices):
        PENDIENTE = 'Pendiente'
        ESPERA = 'Espera de Revision'
        REVISADA = 'Revisada'

    estadoActividad = models.CharField(max_length=50,choices=EstadoActividad.choices,default=EstadoActividad.PENDIENTE)

    dimesion = models.ForeignKey(simpleModels.Dimension,on_delete=models.RESTRICT)
    responsable = models.ForeignKey(authModels.DirectoryUser,related_name='responsable',on_delete=models.RESTRICT)
    participantes = models.ManyToManyField(authModels.DirectoryUser,related_name='participantesActividades')
    area = models.ForeignKey(simpleModels.Area,on_delete=models.RESTRICT)

    actividadPadre = models.ForeignKey('Actividad',on_delete=models.RESTRICT)
    asistencias = models.ManyToManyField(userModels.PosibleGraduado,related_name='asistenciasFamiliarizacion')

class Comentario(abstractModels.AbtractUserForeignKey):
    texto = models.CharField(max_length=255)
    plan = models.ForeignKey(Plan,null=True,blank=True,default=None,on_delete=models.RESTRICT)
    actividad = models.ForeignKey(Actividad,null=True,blank=True,default=None,on_delete=models.RESTRICT)

class Entregable(models.Model):
    archivo = models.FileField()
    ruta = models.FilePathField()
    actividad = models.ForeignKey(Actividad,on_delete=models.RESTRICT)

class FirmadoPor(abstractModels.AbtractUserForeignKey):
    plan = models.ForeignKey(Plan,on_delete=models.RESTRICT)
    aceptado = models.BooleanField(null=True)
