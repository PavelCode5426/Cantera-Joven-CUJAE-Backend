from django.db import models
from custom.authentication import models as authModels
from . import modelosAbstractos as abstractModel
from . import modelosSimple as simpleModels

class Estudiante(authModels.DirectoryUser):
    anno_academico = models.PositiveSmallIntegerField()

class Graduado(authModels.DirectoryUser):
    esExterno = models.BooleanField(default=False)
    esNivelSuperior = models.BooleanField(default=False)

class PosibleGraduado(authModels.DirectoryUser):
    lugarProcedencia = models.ForeignKey(simpleModels.LugarProcedencia,on_delete=models.RESTRICT)
    evaluacionFamiliarizacion = models.ForeignKey('Evaluacion',on_delete=models.RESTRICT,null=True,blank=True)

class Aval(abstractModel.AbtractUserForeignKey):
    indiceAcademico = models.FloatField(default=None,null=True,blank=True)
    esMilitante = models.BooleanField(default=False)
    departamento_AA = models.CharField(max_length=1000,blank=True,null=True,default='')
    factoresUniversitarios = models.BooleanField(default=False)
    factoresTrayectoria = models.BooleanField(default=False)
    participoTareasImpacto = models.BooleanField(default=False)
    cargosEstudiante = models.CharField(max_length=1000,blank=True,null=True,default='')
    cargosMilitante = models.CharField(max_length=1000,blank=True,null=True,default='')
    resumenDesempeno = models.CharField(max_length=1000,blank=True,null=True,default='')