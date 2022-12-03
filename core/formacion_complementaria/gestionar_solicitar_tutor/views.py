from django.db.models import Q
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.models.modelosTutoria import SolicitudTutorExterno, GraduadoTutor
from core.formacion_complementaria.base.permissions import GraduateOfSameAreaPermissions, \
    TutorOfSameAreaPermissions, IsSameTutorWhoRequestPermissions, IsSameGraduateWhoRequestPermissions
from custom.authentication import serializer as authSerializers
from custom.authentication.models import DirectoryUser
from . import serializers
from .exceptions import PreviouslyAnsweredRequestException
from .filters import SolicitudTutorFilterSet, TutoriaFilterSet
from .permissions import SendOrReciveSolicitudTutorExternoPermissions
from ...base.permissions import IsJefeArea, IsSameAreaPermissions, IsDirectorRecursosHumanos


class TutoresPorAreaListAPIView(ListAPIView):
    """
    Lista los Tutores del Area, solamente tendran acceso los jefes de area, podiendo ver solamente en su area.
    """
    serializer_class = authSerializers.DirectoryUserSerializer
    permission_classes = (IsSameAreaPermissions, IsJefeArea)

    def get_queryset(self):
        areaID = self.kwargs['areaID']
        return DirectoryUser.objects.filter(area=areaID, graduado=None, posiblegraduado=None, estudiante=None).all()


class TutoresPorGraduadoListAPIView(ListAPIView):
    """
    Lista los Tutores del Graduado. Solamente tienen acceso el mismo graduado o los jefes de area del graduado.
    """
    serializer_class = serializers.TutoresDelGraduadoSerializer
    permission_classes = (GraduateOfSameAreaPermissions, (IsJefeArea | IsSameGraduateWhoRequestPermissions))
    filterset_class = TutoriaFilterSet

    def get_queryset(self):
        graduado = self.kwargs['graduado']
        return GraduadoTutor.objects.filter(graduado=graduado).order_by('-fechaAsignado').all()


class TutoradosPorTutorListAPIView(ListAPIView):
    """
    Lista los Graduados del Tutor, solamente tendran acceso los jefes de area de su area y el propio tutor
    """
    serializer_class = serializers.TutoradosDelTutorSerializer
    permission_classes = (TutorOfSameAreaPermissions | IsJefeArea | IsSameTutorWhoRequestPermissions)
    filterset_class = TutoriaFilterSet

    def get_queryset(self):
        tutor = self.kwargs['tutor']
        return GraduadoTutor.objects.filter(tutor=tutor).order_by('-fechaAsignado').all()


class AsignarSolicitarTutores(CreateAPIView):
    """
    Permite asignar y solicitar un tutor a un graduado. Solamente tendra acceso el jefe de area
    perteneciente al area del graduado que se le asignara tutores o solicitara tutores.

    Esta interfaz modifica por completo los tutores asignando solamente los que se pasen en la lista.
    En caso de querer eliminar un tutor simplemente no lo envie en la lista.

    """
    serializer_class = serializers.AsignarSolicitarTutorSerializer
    permission_classes = (GraduateOfSameAreaPermissions, IsJefeArea)

    def create(self, request, graduado, **kwargs):
        data = request.data
        data.setdefault('graduado', graduado)
        serializer = serializers.AsignarSolicitarTutorSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)

        result = serializer.save()
        if 'tutores' in result:
            result['tutores'] = 'Tutores asignados correctamente'
        if 'solicitudes' in result:
            result['solicitudes'] = 'Tutores externos solicitados correctamente'

        return Response(result, HTTP_200_OK)


class SolicitudesTutorListAPIView(ListAPIView):
    """
    Permite listar y filtrar todas las solicitudes de tutor recibidas y enviadas. Esta interfaz solamente sera
    accesible para los jefes de area.
    
    TODO TRATAR DE ARREGLAR PARA QUE NO FALLE LA CONSULTA CUANDO LA REALIZA UN DIRECTOR DE RECURSOS HUMANOS

    """
    serializer_class = serializers.SolicitudTutorExternoWithoutMotivoSerializer
    filterset_class = SolicitudTutorFilterSet
    permission_classes = (IsSameAreaPermissions, IsJefeArea | IsDirectorRecursosHumanos)

    def get_queryset(self):
        area = self.kwargs['area'] if 'area' in self.kwargs else self.request.user.area_id
        query = SolicitudTutorExterno.objects.filter(Q(graduado__area_id=area) | Q(area_id=area)) \
            .order_by('-fechaCreado').all()
        return query


class ObtenerResponderSolicitudesTutor(RetrieveAPIView, CreateAPIView):
    """
    Permite obtener y responder las solicitudes de tutor, solamente pueden acceder a las solicitudes los jefes de area
    que la reciban o la envie.
    En el caso de responder la solicitud solamente podran responderla quien la recibieron.


    """
    serializer_class = serializers.SolicitudTutorExternoSerializer
    permission_classes = (SendOrReciveSolicitudTutorExternoPermissions, IsJefeArea)
    lookup_url_kwarg = ('solicitudID')
    lookup_field = 'pk'

    def get_area(self):
        return self.request.user.area

    def get_object(self):
        solicitud = self.kwargs['solicitud'] if 'solicitud' in self.kwargs else None
        if not solicitud:
            solicitud = get_object_or_404(SolicitudTutorExterno, pk=self.kwargs['solicitudID'])
        return solicitud

    def create(self, request, solicitud, **kwargs):
        """
        RESPONDER LA SOLICITUD DE TUTOR.
        """
        if solicitud.respuesta is not None:
            raise PreviouslyAnsweredRequestException

        data = request.data
        data['area'] = self.get_area()
        data['solicitud'] = solicitud

        serializer = serializers.ResponderSolicitudSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)

        solicitud = serializer.save()

        return Response({'detail': 'Solicitud {resp} correctamente'.format(
            resp='aceptada' if solicitud.respuesta else 'rechazada')}, HTTP_200_OK)
