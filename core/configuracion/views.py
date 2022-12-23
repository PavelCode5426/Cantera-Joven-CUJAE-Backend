from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response

from core.base import permissions
from core.base.models import modelosSimple
from . import serializers
# Create your views here.
from .proxy import ConfigurationProxy
from .signals import configuracion_actualizada


class GestionarConfiguracion(ListCreateAPIView, UpdateAPIView):
    permission_classes = [permissions.IsDirectorRecursosHumanos]
    serializer_class = serializers.ConfigurationSerializer
    queryset = modelosSimple.Configuracion.objects.all().order_by('created_at')
    pagination_class = None

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        ConfigurationProxy().load_config()
        return response

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        configuracion_actualizada.send(instance)
        return Response(serializer.data)
