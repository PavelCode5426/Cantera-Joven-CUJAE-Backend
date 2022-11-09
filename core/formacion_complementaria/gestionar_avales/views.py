from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from core.base.models import modelosUsuario
from core.base.permissions import IsDirectorRecursosHumanos
from custom.authentication import models as authModels
from .permissions import IsAvalOwnerOrJefeArea
from .serializers import UserAvalSerializer, PlantillaAvalSerializer


class PlantillaAvalModelViewSet(ModelViewSet):
    serializer_class = PlantillaAvalSerializer
    queryset = modelosUsuario.PlantillaAval.objects.all()
    pagination_class = None


class ObtenerCrearActualizarAval(CreateAPIView, RetrieveUpdateAPIView):
    serializer_class = UserAvalSerializer
    lookup_url_kwarg = ['usuario']
    permission_classes = [IsAvalOwnerOrJefeArea | IsDirectorRecursosHumanos]

    def __get_usuario(self):
        return self.kwargs.get('usuario', None)

    def get_object(self):
        aval = get_object_or_404(modelosUsuario.Aval, usuario_id=self.__get_usuario())
        return aval

    def create(self, request, usuario):
        data = request.data
        usuario = get_object_or_404(authModels.DirectoryUser, pk=usuario)
        data.setdefault('usuario', usuario)
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response({'detail': 'Aval creado correctamente'}, HTTP_200_OK)

        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
