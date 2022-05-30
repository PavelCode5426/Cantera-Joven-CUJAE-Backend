from .serializers import AreaSerializer
from core.base.models import modelosSimple
from rest_framework.viewsets import mixins,GenericViewSet

class ListarObtenerArea(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    serializer_class = AreaSerializer
    queryset = modelosSimple.Area.objects.all()


