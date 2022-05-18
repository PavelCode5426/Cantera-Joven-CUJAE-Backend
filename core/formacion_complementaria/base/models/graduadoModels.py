from custom.authentication.models import DirectoryUser
from django.db import models


class Graduado(DirectoryUser):
    is_universitario = models.BooleanField()


class GraduadoTutor(models.Model):
    graduado = models.ForeignKey(Graduado,models.CASCADE,editable=False,related_name='tutorado')
    tutor = models.ForeignKey(DirectoryUser,models.CASCADE,editable=False,related_name='tutor')

    fecha_asignacion = models.DateTimeField(auto_now=True,editable=False)
    fecha_revocacion = models.DateTimeField(default=None,null=True,blank=True)


