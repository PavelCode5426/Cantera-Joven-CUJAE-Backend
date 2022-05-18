from django.db import models

from custom.authentication.models import DirectoryUser
# Create your models here.

class NameEntity(models.Model):
    nombre = models.CharField(max_length=100,unique=True)
    class Meta:
        abstract = True

class Area(NameEntity):
    pass

class LugarProcedencia(NameEntity):
    pass

class Registro(models.Model):
    accion = models.CharField(max_length=100,editable=False)
    fecha = models.DateTimeField(auto_now=True,editable=False)

    usuario = models.ForeignKey(DirectoryUser,models.CASCADE,editable=False)

#CAMBIAR DIAGRAMA, EN EL MODELADO SE DECIDIO CREAR UN CHOOSER
#ESTOY HABLANDO DE LA ENTIDAD ESTADO ;)
ESTADOS_DEL_PLAN = (
    ('C','CREADO'),
    ('A','APROBADO'),
    ('E','EJECUCION'),
    ('R','RECHAZADO')
)

class Plan(models.Model):
    estado = models.CharField(max_length=50,choices=ESTADOS_DEL_PLAN)
    fecha_creado = models.DateTimeField(auto_now=True,editable=False)
    #INCLUI ESTE ATRIBUTO PARA GUARDAR LA FECHA EXACTA DE CREACION
    #ESO NO SIGNIFICA QUE NO SE PUEDA AGREGAR EL AÑO EN LOS OTROS PLANES

class Actividad(models.Model):
    nombre = models.CharField(max_length=255)
    responsable = models.ManyToManyField(DirectoryUser)
    descripcion = models.CharField(max_length=250)
    fecha_inicio = models.DateTimeField()

class Evaluacion(models.Model):
    texto = models.CharField(max_length=250)

class Etapa(models.Model):
    numero = models.PositiveSmallIntegerField(default=1)
    objetivo = models.CharField(max_length=250)
    fecha_inicio = models.DateTimeField(auto_now=True)
    fecha_final = models.DateTimeField(default=None,null=True,blank=True)

    evaluacion = models.ForeignKey(Evaluacion,models.PROTECT,default=None,null=True,blank=True)


class Confeccion(models.Model):
    firmado = models.BooleanField(default=False)
    usuario = models.ForeignKey(DirectoryUser,models.PROTECT)


class Dimension(NameEntity):
    pass


ESTADOS_DEL_TAREAS_FORMACION_CANTERA = (
    ('P','PENDIENTE'),
    ('E','EJECUCION'),
    ('C','COMPLETADA'),
)
class ActividadCanteraFormacionComplementaria(Actividad):
    fecha_cumplimiento = models.DateTimeField(default=None,null=True,blank=True)
    fecha_fin = models.DateTimeField()

    tarea_padre = models.ForeignKey('self',models.PROTECT)
    etapa = models.ForeignKey(Etapa,models.PROTECT)
    dimension = models.ForeignKey(Dimension,models.PROTECT)
    estado = models.CharField(max_length=50,choices=ESTADOS_DEL_TAREAS_FORMACION_CANTERA)

    participantes = models.ManyToManyField(DirectoryUser)


class Entregable(models.Model):
    tarea = models.ForeignKey(ActividadCanteraFormacionComplementaria,on_delete=models.PROTECT)
    archivo = models.FileField(upload_to='entregables/%Y/%m/%d')


























