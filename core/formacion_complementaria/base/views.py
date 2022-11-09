from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.models.modelosSimple import Area
from core.base.models.modelosUsuario import Graduado
from core.base.permissions import IsDirectorRecursosHumanos, IsJefeArea
from core.formacion_complementaria.base.filters import GraduadoFilterSet
from core.formacion_complementaria.base.permissions import IsSameAreaPermissions
from core.formacion_complementaria.base.serializers import ImportarGraduadoSerializer, GraduadoSerializer
from custom.authentication.directorio.graduado import obtenerGraduado, obtenerTodosGraduados


# TODO TENGO QUE REVISAR LAS IMPORTACIONES DEL SIGENU

class GraduadosEnDirectorio(ListCreateAPIView, RetrieveAPIView):
    permission_classes = [IsDirectorRecursosHumanos]

    def list(self, request):
        graduados = obtenerTodosGraduados()
        sinIncorporar = list()

        for graduado in graduados:
            try:
                Graduado.objects.get(directorioID=graduado['id'])
            except Graduado.DoesNotExist:
                sinIncorporar.append(graduado)

        return Response(sinIncorporar, HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = ImportarGraduadoSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail': 'Graduados importados correctamente'}, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)

    def retrieve(self, request, graduadoID):
        graduado = obtenerGraduado(graduadoID)
        if graduado:
            return Response(graduado, HTTP_200_OK)
        return Response({'detail': 'No encontrado'}, HTTP_400_BAD_REQUEST)


class ListGraduadosDelArea(ListAPIView):
    serializer_class = GraduadoSerializer
    permission_classes = (IsSameAreaPermissions, IsJefeArea)
    # FILTRADO
    filterset_class = GraduadoFilterSet
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering_fields = '__all__'

    def get_queryset(self):
        area = get_object_or_404(Area, pk=self.kwargs['areaID'])
        return Graduado.objects.filter(area=area).distinct()
