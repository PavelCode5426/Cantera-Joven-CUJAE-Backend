from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from core.base.models import modelosUsuario, modelosSimple
from . import serializers
from ...base.permissions import IsDirectorRecursosHumanos, IsJefeArea
from ...formacion_complementaria.gestionar_solicitar_tutor.views import CustomListAPIView


class ListEstudiantesSinAval(ListAPIView):
    permission_classes = [IsDirectorRecursosHumanos]
    serializer_class = serializers.EstudianteSerializer
    queryset = modelosUsuario.Estudiante.objects.filter(aval=None).all()


class ListEstudiantesDelArea(CustomListAPIView):
    permission_classes = [IsJefeArea | IsDirectorRecursosHumanos]
    serializer_class = serializers.EstudianteSerializer

    def list(self, request, *args, **kwargs):
        area = self.get_area()
        estudiante = modelosUsuario.Estudiante.objects.filter(area=area)
        serializer = self.serializer_class(estudiante, many=True)
        return Response(serializer.data, HTTP_200_OK)


class ListEstudinatesDelAreaSinAval(CustomListAPIView):
    permission_classes = [IsJefeArea | IsDirectorRecursosHumanos]
    serializer_class = serializers.EstudianteSerializer

    def list(self, request, areaID=None):
        area = get_object_or_404(modelosSimple.Area, pk=areaID) if areaID else self.get_area()
        esttudiante = modelosUsuario.Estudiante.objects.filter(aval=None, area=area).all()
        serializer = self.get_serializer(esttudiante, many=True)
        return Response(serializer.data, HTTP_200_OK)
