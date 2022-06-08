from django.utils.timezone import now
from rest_framework import serializers
from core.base.models.modelosUsuario import Estudiante
from core.base.models.modelosSimple import Area

from custom.authentication.serializer import DirectoryUserSerializer
from custom.authentication.models import DirectoryUser

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ('id','username','first_name','last_name','email','anno_academico','aval')