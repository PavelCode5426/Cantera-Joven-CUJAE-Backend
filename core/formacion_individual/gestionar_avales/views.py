from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from core.base.models import modelosUsuario
from core.base.permissions import IsDirectorRecursosHumanos
from custom.authentication import models as authModels
from .permissions import IsAvalOwner, IsAvalOwnerTutorOrJefeArea
from .serializers import UserAvalSerializer, PlantillaAvalSerializer
from ...base.generics import MultiplePermissionsView


class PlantillaAvalModelViewSet(ModelViewSet):
    serializer_class = PlantillaAvalSerializer
    queryset = modelosUsuario.PlantillaAval.objects.all()
    pagination_class = None


class ObtenerCrearActualizarAval(CreateAPIView, RetrieveUpdateAPIView, MultiplePermissionsView):
    # TODO REVISAR LOS PERMISOS DE LOS AVALES
    serializer_class = UserAvalSerializer
    lookup_url_kwarg = ['usuarioID']
    permission_classes = [IsAvalOwner | IsAvalOwnerTutorOrJefeArea | IsDirectorRecursosHumanos]

    def __get_usuario(self):
        return self.kwargs.get('usuarioID', None)

    def get_object(self):
        aval = get_object_or_404(modelosUsuario.Aval, usuario_id=self.__get_usuario())
        return aval

    def create(self, request, usuarioID):
        data = request.data
        usuario = get_object_or_404(authModels.DirectoryUser, pk=usuarioID)
        data.setdefault('usuario', usuario)
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response({'detail': 'Aval creado correctamente'}, HTTP_200_OK)

        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
