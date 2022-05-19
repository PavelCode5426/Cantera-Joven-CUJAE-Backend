from custom.authentication.models import DirectoryUser
from django.db import models


class Estudiante(DirectoryUser):
    anno_academico = models.IntegerField(Default=0)