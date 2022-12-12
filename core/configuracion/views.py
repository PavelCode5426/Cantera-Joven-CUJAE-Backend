from rest_framework.generics import ListCreateAPIView, UpdateAPIView

from core.base import permissions
from core.base.models import modelosSimple
from . import serializers
# Create your views here.
from .proxy import ConfigurationProxy


class GestionarConfiguracion(ListCreateAPIView, UpdateAPIView):
    permission_classes = [permissions.IsDirectorRecursosHumanos]
    serializer_class = serializers.ConfigurationSerializer
    queryset = modelosSimple.Configuracion.objects.all().order_by('created_at')
    pagination_class = None

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        ConfigurationProxy().load_config()
        return response
