from rest_framework.generics import ListCreateAPIView,RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.models.modelosUsuario import Graduado
from core.formacion_complementaria.base.serializers import ImportarGraduadoSerializer
from custom.authentication.directorio.graduado import obtenerGraduados, obtenerGraduado, obtenerTodosGraduados


class GraduadosEnDirectorio(ListCreateAPIView):
    def list(self, request):
        graduados = obtenerTodosGraduados()
        sinIncorporar = list()

        for graduado in graduados:
            try:
                Graduado.objects.get(directorioID=graduado['id'])
            except Graduado.DoesNotExist:
                sinIncorporar.append(graduado)

        return Response(sinIncorporar,HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = ImportarGraduadoSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail':'Graduados importados correctamente'},HTTP_200_OK)
        else: return Response(serializer.errors,HTTP_400_BAD_REQUEST)

class ObtenerGraduadoEnDirectorio(RetrieveAPIView):
    def retrieve(self, request,graduadoID):
        graduado = obtenerGraduado(graduadoID)
        if graduado:
            return Response(graduado, HTTP_200_OK)
        return Response({'detail':'No encontrado'},HTTP_400_BAD_REQUEST)