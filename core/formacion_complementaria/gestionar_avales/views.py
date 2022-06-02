from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from .serializers import UserAvalSerializer
from core.base.models import modelosUsuario
from custom.authentication import models as authModels

# Create your views here.
class ObtenerCrearActualizarAval(CreateAPIView,RetrieveUpdateAPIView):
    serializer_class = UserAvalSerializer
    lookup_url_kwarg = ['usuario']

    def __get_usuario(self):
        return self.kwargs.get('usuario',None)

    def get_object(self):
        aval = get_object_or_404(modelosUsuario.Aval,usuario_id=self.__get_usuario())
        return aval

    def create(self, request, *args, **kwargs):
        data = request.data
        usuario = authModels.DirectoryUser.objects.get(pk=self.__get_usuario())
        data.setdefault('usuario', usuario)
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data.setdefault('usuario',usuario)
            serializer.create(validated_data)
            return Response(serializer.data,HTTP_200_OK)

        return Response(serializer.errors,HTTP_400_BAD_REQUEST)
