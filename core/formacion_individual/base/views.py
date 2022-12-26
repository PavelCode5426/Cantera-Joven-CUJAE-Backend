from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.models.modelosSimple import Area
from core.base.models.modelosUsuario import Graduado, Estudiante
from core.base.permissions import IsDirectorRecursosHumanos, IsJefeArea, IsSameAreaPermissions
from core.formacion_individual.base.filters import JovenFilterSet, JovenAdvanceFilterSet
from core.formacion_individual.base.serializers import ImportarGraduadoSerializer, GraduadoSerializer, \
    ImportarTutorSerializer, ImportarEstudianteSerializer, EstudianteSerializer, JovenSerializer
from custom.authentication.LDAP.ldap_facade import LDAPFacade
from custom.authentication.models import DirectoryUser


class ImportarGraduadosDirectorio(ListCreateAPIView):
    permission_classes = [IsDirectorRecursosHumanos]

    def list(self, request, **kwargs):
        graduados = LDAPFacade().all_graduates()
        importados = Graduado.objects.filter(directorioID__in=[grad['areaId'] for grad in graduados])

        sin_importar = []
        for element in graduados:
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
        serializer = ImportarGraduadoSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail': 'Graduados importados correctamente'}, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class ImportarTutoresDirectorio(ListCreateAPIView):
    permission_classes = (IsSameAreaPermissions, IsJefeArea | IsDirectorRecursosHumanos)

    # NO SE LE PUSO FILTRO PORQUE HARIA MAS COMPLEJA LA CONSULTA O TARDARIA MAS. EL FRONT QUE FILTRE
    def list(self, request, **kwargs):
        area = kwargs['area']
        tutores = LDAPFacade().all_tutors_from_area(area)
        importados = DirectoryUser.objects.filter(directorioID__in=[tutor['areaId'] for tutor in tutores])

        sin_importar = []
        for element in tutores:
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
        serializer = ImportarTutorSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail': 'Tutores importados correctamente'}, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class ListGraduadosDelArea(ListAPIView):
    serializer_class = GraduadoSerializer
    permission_classes = (IsSameAreaPermissions, IsJefeArea | IsDirectorRecursosHumanos)
    # FILTRADO
    filterset_class = JovenFilterSet
    search_fields = ('first_name', 'last_name', 'email', 'username', 'carnet')
    ordering_fields = '__all__'

    def get_queryset(self):
        area = get_object_or_404(Area, pk=self.kwargs['areaID'])
        # TODO HAZ QUE SOLAMENTE SALGAN LOS QUE NO SEAN TUTORES, PARA ESTO USA LA TABLA DE TUTORES ASIGNADOS
        return Graduado.objects.filter(area=area).distinct()


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
    permission_classes = (IsSameAreaPermissions, IsJefeArea | IsDirectorRecursosHumanos)
    serializer_class = EstudianteSerializer
    filterset_class = JovenFilterSet
    search_fields = ('first_name', 'last_name', 'email', 'username', 'carnet')
    ordering_fields = '__all__'

    def get_queryset(self):
        area = get_object_or_404(Area, pk=self.kwargs['areaID'])
        return Estudiante.objects.filter(area=area).distinct()


class ListJovenesDelArea(ListAPIView):
    """
    Lista los Jovenes del Area, solamente tendran acceso los jefes de area, podiendo ver solamente en su area.
    """
    serializer_class = JovenSerializer
    permission_classes = (IsSameAreaPermissions, IsJefeArea)
    filterset_class = JovenAdvanceFilterSet
    search_fields = ('first_name', 'last_name', 'email', 'username', 'carnet')
    ordering_fields = '__all__'
    #TODO Pavel revisar esto, el serializador cunado es un graduado no da todo pero para el estudiante si da las cosas
    def get_queryset(self):
        areaID = self.kwargs['areaID']
        return DirectoryUser.objects.select_related('grduado','estudiante').filter(Q(graduado__isnull=False) | Q(estudiante__isnull=False),
                                            area=areaID).distinct().all()
