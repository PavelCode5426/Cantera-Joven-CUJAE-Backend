from django.db import models
from custom.authentication import models as authModels

class AbtractUserForeignKey(models.Model):
    usuario = models.ForeignKey(authModels.DirectoryUser,on_delete=models.RESTRICT)
    class Meta:
        abstract = True

class AbstractNameEntity(models.Model):
    nombre = models.CharField(max_length=255)
    class Meta:
        abstract = True