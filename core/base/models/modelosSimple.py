from django.db import models

from . import modelosAbstractos as abstractModels


class Area(abstractModels.AbstractNameEntity):
    distinguishedName = models.CharField(max_length=255)

    def __str__(self):
        return self.distinguishedName


class PropuestaMovimiento(abstractModels.AbstractNameEntity):
    pass


class Dimension(abstractModels.AbstractNameEntity):
    pass


class Configuracion(models.Model):
    etiqueta = models.CharField(max_length=250, unique=True)
    valor = models.JSONField()
    validacion = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

class Carrera(abstractModels.AbstractNameEntity):
    codigo = models.CharField(max_length=100)

