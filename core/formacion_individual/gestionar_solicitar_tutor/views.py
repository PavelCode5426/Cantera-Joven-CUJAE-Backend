from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from core.base.models.modelosPlanificacionIndividual import SolicitudTutorExterno, TutoresAsignados
from core.formacion_individual.base.permissions import JovenOfSameAreaPermissions, \
    TutorOfSameAreaPermissions, IsSameTutorWhoRequestPermissions, IsSameJovenWhoRequestPermissions
from custom.authentication import serializer as authSerializers
from custom.authentication.models import DirectoryUser
from . import serializers
from .exceptions import PreviouslyAnsweredRequestException, GraduateRequireAvalException, \
    SelectedUserIsNotJovenException
from .filters import SolicitudTutorFilterSet, TutoriaFilterSet, TutoriaPorTutorFilterSet
from .permissions import SendOrReciveSolicitudTutorExternoPermissions
from ..base.helpers import user_student_or_graduate
from ...base.models.modelosUsuario import Graduado
from ...base.permissions import IsJefeArea, IsSameAreaPermissions, IsDirectorRecursosHumanos


class TutoresPorAreaListAPIView(ListAPIView):
    """
    Lista los Tutores del Area, solamente tendran acceso los jefes de area, podiendo ver solamente en su area.
    """
    serializer_class = authSerializers.DirectoryUserSerializer
    permission_classes = (IsSameAreaPermissions, IsJefeArea)
    search_fields = ('first_name', 'last_name', 'email', 'username', 'carnet')
    ordering_fields = '__all__'

    def get_queryset(self):
        areaID = self.kwargs['areaID']
        return DirectoryUser.objects.filter(area=areaID, graduado=None, posiblegraduado=None, estudiante=None).all()


class TutoresPorGraduadoListAPIView(ListAPIView):
    """
    Lista los Tutores del Graduado. Solamente tienen acceso el mismo graduado o los jefes de area del graduado.
    """
    serializer_class = serializers.TutoresDelGraduadoSerializer
    permission_classes = (JovenOfSameAreaPermissions, (IsJefeArea | IsSameJovenWhoRequestPermissions),)
    filterset_class = TutoriaFilterSet
    search_fields = ('tutor__first_name', 'tutor__last_name', 'tutor__email', 'tutor__username', 'tutor__carnet')
    ordering_fields = '__all__'

    def get_queryset(self):
        joven_id = self.kwargs['jovenID']
        return TutoresAsignados.objects.filter(joven_id=joven_id).order_by('-fechaAsignado').all()


class TutoradosPorTutorListAPIView(ListAPIView):
    """
    Lista los Graduados del Tutor, solamente tendran acceso los jefes de area de su area y el propio tutor
    """
    serializer_class = serializers.TutoradosDelTutorSerializer
    permission_classes = (TutorOfSameAreaPermissions | IsJefeArea | IsSameTutorWhoRequestPermissions,)
    filterset_class = TutoriaPorTutorFilterSet
    search_fields = ('joven__first_name', 'joven__last_name', 'joven__email', 'joven__username', 'joven__carnet')
    ordering_fields = '__all__'

    def get_queryset(self):
        tutor = self.kwargs['tutor']
        return TutoresAsignados.objects.filter(tutor=tutor).order_by('-fechaAsignado').all()


class AsignarSolicitarTutores(CreateAPIView):
    """
    Permite asignar y solicitar un tutor a un graduado. Solamente tendra acceso el jefe de area
    perteneciente al area del graduado que se le asignara tutores o solicitara tutores.

    Esta interfaz modifica por completo los tutores asignando solamente los que se pasen en la lista.
    En caso de querer eliminar un tutor simplemente no lo envie en la lista.

    """
    serializer_class = serializers.AsignarSolicitarTutorSerializer
    permission_classes = (JovenOfSameAreaPermissions, IsJefeArea)

    def create(self, request, *args, **kwargs):
        joven, es_estudiante = user_student_or_graduate(kwargs.get('joven'))

        if not joven:
            raise SelectedUserIsNotJovenException
        elif isinstance(joven, Graduado) and not hasattr(joven, 'aval') and joven.esNivelSuperior:
            raise GraduateRequireAvalException

        data = request.data
        data.setdefault('joven', joven)
        serializer = serializers.AsignarSolicitarTutorSerializer(data=data)
        serializer.is_valid(True)
        result = serializer.save(joven=joven)
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
    permission_classes = (IsSameAreaPermissions, IsJefeArea | IsDirectorRecursosHumanos,)
    search_fields = (
        'area__nombre', 'joven__area_nombre', 'joven__first_name', 'joven__last_name', 'joven__email',
        'joven__username',
        'joven__carnet')
    ordering_fields = '__all__'

    def get_queryset(self):
        area = self.kwargs.get('areaID', self.request.user.area_id)
        query = SolicitudTutorExterno.objects.all()
        # query = SolicitudTutorExterno.objects.filter(Q(joven__area_id=area) | Q(area_id=area)).order_by('-fechaCreado').all()
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
        serializer.is_valid(True)
        solicitud = serializer.save()

        return Response({'detail': 'Solicitud {resp} correctamente'.format(
            resp='aceptada' if solicitud.respuesta else 'rechazada')}, HTTP_200_OK)
