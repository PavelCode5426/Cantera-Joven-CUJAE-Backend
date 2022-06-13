from rest_framework import serializers
from core.base.models.modelosUsuario import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ('id','username','first_name','last_name','email','anno_academico','aval')