from rest_framework.generics import ListCreateAPIView,RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from custom.authentication.directorio.estudiante import obtenerEstudiante,obtenerEstudiantes
from .serializers import ImportarEstudianteSerializer

class EstudiantesEnDirectorio(ListCreateAPIView):
    def list(self, request):
        items = obtenerEstudiantes()
        return Response(items,HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = ImportarEstudianteSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail':'Estudiantes importados correctamente'},HTTP_200_OK)
        else: return Response(serializer.errors,HTTP_400_BAD_REQUEST)

class EstudianteEnDirectorio(RetrieveAPIView):
    def retrieve(self, request,estudianteID):
        graduado = obtenerEstudiante(estudianteID)
        if graduado:
            return Response(graduado, HTTP_200_OK)
        return Response({'detail':'No encontrado'},HTTP_400_BAD_REQUEST)









