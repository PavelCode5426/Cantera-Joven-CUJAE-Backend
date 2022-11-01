from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.models.modelosUsuario import PosibleGraduado
from custom.authentication.directorio.posibleGraduado import obtenerPosibleGraduado, \
    obtenerTodosPosibleGraduados
from .serializers import ImportarPosibleGraduadoSerializer
from ...base.permissions import IsDirectorRecursosHumanos


class PosiblesGraduadosEnDirectorio(ListCreateAPIView):
    permission_classes = [IsDirectorRecursosHumanos]

    def list(self, request):
        posiblesGraduados = obtenerTodosPosibleGraduados()
        sinIncorporar = list()

        for posiblesGraduado in posiblesGraduados:
            try:
                PosibleGraduado.objects.get(directorioID=posiblesGraduado['id'])
            except PosibleGraduado.DoesNotExist:
                sinIncorporar.append(posiblesGraduado)

        return Response(sinIncorporar, HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = ImportarPosibleGraduadoSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail': 'Posibles graduados importados correctamente'}, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class PosibleGraduadoEnDirectorio(RetrieveAPIView):
    permission_classes = [IsDirectorRecursosHumanos]

    def retrieve(self, request, posibleGraduadoID):
        posibleGraduado = obtenerPosibleGraduado(posibleGraduadoID)
        if posibleGraduado:
            return Response(posibleGraduado, HTTP_200_OK)
        return Response({'detail': 'No encontrado'}, HTTP_400_BAD_REQUEST)
