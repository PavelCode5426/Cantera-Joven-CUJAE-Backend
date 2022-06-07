from django.db import models

class AbtractUserForeignKey(models.Model):
    usuario = models.ForeignKey("authentication.DirectoryUser",on_delete=models.RESTRICT)
    class Meta:
        abstract = True

class AbstractNameEntity(models.Model):
    nombre = models.CharField(max_length=100)
    class Meta:
        abstract = True