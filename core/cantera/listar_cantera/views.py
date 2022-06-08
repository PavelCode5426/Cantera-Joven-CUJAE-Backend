from django.db.models import Q
from django.utils.timezone import now
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.models.modelosUsuario import Estudiante
from core.base.models import modelosUsuario,modelosSimple
from . import serializers

class ListEstudiantesSinAval(ListAPIView):
    serializer_class = serializers.EstudianteSerializer
    queryset = modelosUsuario.Estudiante.objects.filter(aval=None).all()

