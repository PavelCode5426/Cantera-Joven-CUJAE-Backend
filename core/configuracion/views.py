from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from core.base import permissions
from core.base.models import modelosSimple
from . import serializers


# Create your views here.


class GestionarConfiguracion(ListCreateAPIView, UpdateAPIView):
    permission_classes = [permissions.IsDirectorRecursosHumanos]
    serializer_class = serializers.ConfigurationSerializer
    queryset = modelosSimple.Configuracion.objects.all()

    def list(self, request, *args, **kwargs):
        list = dict()
        for configItem in self.get_queryset():
            list.setdefault(configItem.llave,
                            {
                                'id': configItem.id,
                                'valor': configItem.valor
                            })
        return Response(list, HTTP_200_OK)
