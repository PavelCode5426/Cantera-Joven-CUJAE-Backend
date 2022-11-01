from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from core.base.models.modelosUsuario import Estudiante
from custom.authentication.directorio.estudiante import obtenerEstudiante, obtenerTodosEstudiantes
from .serializers import ImportarEstudianteSerializer
from ...base.permissions import IsDirectorRecursosHumanos


class EstudiantesEnDirectorio(ListCreateAPIView):
    permission_classes = [IsDirectorRecursosHumanos]
    '''
    TODO FILTRAR, PERO HAY QUE HABLAR CON PICAYO PARA SABER QUE RETORNA EL DIRECTORIO O EL SIGNU
    '''

    def list(self, request):
        estudiantes = obtenerTodosEstudiantes()
        sinIncorporar = list()

        for estudiante in estudiantes:
            try:
                Estudiante.objects.get(directorioID=estudiante['id'])
            except Estudiante.DoesNotExist:
                sinIncorporar.append(estudiante)

        return Response(sinIncorporar, HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = ImportarEstudianteSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail': 'Estudiantes importados correctamente'}, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class EstudianteEnDirectorio(RetrieveAPIView):
    permission_classes = [IsDirectorRecursosHumanos]

    def retrieve(self, request, estudianteID):
        graduado = obtenerEstudiante(estudianteID)
        if graduado:
            return Response(graduado, HTTP_200_OK)
        return Response({'detail': 'No encontrado'}, HTTP_404_NOT_FOUND)
