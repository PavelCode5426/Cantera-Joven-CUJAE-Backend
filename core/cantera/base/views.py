from rest_framework.generics import ListCreateAPIView, get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.permissions import IsJefeArea, IsSameAreaPermissions, IsDirectorRecursosHumanos
from custom.authentication.LDAP.ldap_facade import LDAPFacade
from custom.authentication.models import DirectoryUser
from .filters import EstudianteFilterSet
from .serializers import ImportarEstudianteSerializer, EstudianteSerializer
from ...base.models.modelosSimple import Area
from ...base.models.modelosUsuario import Estudiante


class ImportarEstudiantesDirectorio(ListCreateAPIView):
    permission_classes = (IsSameAreaPermissions, IsJefeArea)

    # NO SE LE PUSO FILTRO PORQUE HARIA MAS COMPLEJA LA CONSULTA O TARDARIA MAS. EL FRONT QUE FILTRE
    def list(self, request, **kwargs):
        area = kwargs['area']
        estudiantes = LDAPFacade().all_students_from_area(area)
        # PREGUNTO POR EL USUARIO Y NO POR EL ESTUDIANTE PORQUE ESTUDIANTE ES LO MENOS QUE PUEDES SER EN EL SISTEMA
        # POR LO TANTO SI ESTAS EN EL SISTEMA ES PORQUE ERES ALGO DIFERENTE DE ESTUDIANTE O IGUAL A ESTUDIANTE
        importados = DirectoryUser.objects.filter(directorioID__in=[est['areaId'] for est in estudiantes])

        sin_importar = []
        for element in estudiantes:
            found = False
            it = iter(importados)
            try:
                while not found:
                    elem = next(it)
                    if elem.directorioID == element['areaId']:
                        found = True
            except StopIteration:  # SOLAMENTE SE LANZA CUANDO LLEGA AL FINAL
                sin_importar.append(element)

        return Response(sin_importar, HTTP_200_OK)

    def create(self, request, **kwargs):
        data = request.data
        data['area'] = kwargs['area']
        serializer = ImportarEstudianteSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail': 'Estudiantes importados correctamente'}, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class ListEstudiantesDelArea(ListAPIView):
    serializer_class = EstudianteSerializer
    permission_classes = (IsSameAreaPermissions, IsJefeArea | IsDirectorRecursosHumanos)
    filterset_class = EstudianteFilterSet
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering_fields = '__all__'

    def get_queryset(self):
        area = get_object_or_404(Area, pk=self.kwargs['areaID'])
        return Estudiante.objects.filter(area=area).distinct()
