from rest_framework.generics import ListAPIView
from core.base.models import modelosUsuario
from . import serializers

class ListEstudiantesSinAval(ListAPIView):
    serializer_class = serializers.EstudianteSerializer
    queryset = modelosUsuario.Estudiante.objects.filter(aval=None).all()

