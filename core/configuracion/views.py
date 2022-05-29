from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.generics import ListCreateAPIView,UpdateAPIView
from . import serializers
from core.base.models import modelosSimple


# Create your views here.

class GestionarConfiguracion(ListCreateAPIView,UpdateAPIView):
    serializer_class = serializers.ConfigurationSerializer
    queryset = modelosSimple.Configuracion.objects.all()

    def list(self, request, *args, **kwargs):
        list = dict()
        for configItem in self.get_queryset():
            list.setdefault(configItem.llave,
                            {
                                'id':configItem.id,
                                'valor':configItem.valor
                            })
        return Response(list,HTTP_200_OK)

