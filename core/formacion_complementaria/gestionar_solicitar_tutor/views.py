from django.db.models import Q
from django.utils.timezone import now
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.models.modelosUsuario import Graduado
from custom.authentication import serializer as authSerializers
from custom.authentication import models as authModels
from core.base.models import modelosUsuario,modelosSimple
from . import serializers
from core.base.models.modelosTutoria import SolicitudTutorExterno
from core.base.permissions import IsJefeArea, IsTutor, IsGraduado

class CustomListAPIView(ListAPIView):
    def get_area(self):
        area = self.request.user.area
        return area

class ListTutoresArea(CustomListAPIView):
    """Lista los Tutores del Area"""
    permission_classes = [IsJefeArea]
    serializer_class = authSerializers.DirectoryUserSerializer
    def list(self, request, *args, **kwargs):
        area = self.get_area()
        usuarios = authModels.DirectoryUser.objects.filter(area=area,graduado=None,posiblegraduado=None,estudiante=None)
        serializer = self.serializer_class(usuarios,many=True)
        return Response(serializer.data,HTTP_200_OK)

class ListGraduadosDelArea(CustomListAPIView):
    permission_classes = [IsJefeArea, IsTutor]
    serializer_class = serializers.GraduadoSerializer
    def list(self, request, *args, **kwargs):
        area = self.get_area()
        graduados = modelosUsuario.Graduado.objects.filter(area=area)
        serializer = self.serializer_class(graduados,many=True)
        return Response(serializer.data,HTTP_200_OK)

class ListGraduadosSinTutor(CustomListAPIView):
    permission_classes = [IsJefeArea, IsTutor]
    serializer_class = serializers.GraduadoSerializer
    def list(self, request, *args, **kwargs):
        area = self.get_area()
        #FILTRAR PARA QUE NO TENGA TUTOR
        graduados = modelosUsuario.Graduado.objects.filter(area=area)
        serializer = self.serializer_class(graduados, many=True)
        return Response(serializer.data, HTTP_200_OK)

class ListGraduadosSinAval(CustomListAPIView):
    permission_classes = [IsJefeArea, IsTutor]
    serializer_class = serializers.GraduadoSerializer
    queryset = modelosUsuario.Graduado.objects.filter(aval=None)

class ListGraduadosDelAreaSinAval(CustomListAPIView):
    permission_classes = [IsJefeArea, IsTutor]
    serializer_class = serializers.GraduadoSerializer
    def list(self, request,areaID=None):
        area = get_object_or_404(modelosSimple.Area,pk=areaID) if areaID else self.get_area()
        graduados = modelosUsuario.Graduado.objects.filter(aval=None,area=area).all()
        serializer = self.get_serializer(graduados,many=True)
        return Response(serializer.data,HTTP_200_OK)

#TODO Falta proteger la ruta
#Solamente tendran acceso los graduados o jefes de area
class ListTutoresGraduado(ListAPIView):
    permission_classes = [IsJefeArea, IsGraduado]
    """Lista los Tutores del Graduado"""
    serializer_class = serializers.TutoresDelGraduadoSerializer

    def list(self, request, graduado=None, **kwargs):
        if graduado:
            graduado = get_object_or_404(modelosUsuario.Graduado,pk=graduado)
        else:
            try:
                graduado = request.user.graduado
            except modelosUsuario.Graduado.DoesNotExist:
                return Response({'detail':'No cuenta con datos de graduado'},HTTP_400_BAD_REQUEST)

        tutores = graduado.tutores.filter(fechaRevocado=None).all()
        serializer = self.serializer_class(tutores,many=True)
        return Response(serializer.data,HTTP_200_OK)

#TODO Falta proteger la ruta
#Solamente tendran acceso los tutores o jefes de area
class ListGraduadosTutor(ListAPIView):
    permission_classes = [IsJefeArea, IsTutor]
    """Lista los Graduados del Tutor"""
    serializer_class = serializers.GraduadosDelTutorSerializer

    def list(self, request, tutor=None, **kwargs):
        if tutor:
            tutor = get_object_or_404(authModels.DirectoryUser, pk=tutor)
        else:
            tutor = request.user

        graduados = tutor.graduados.filter(fechaRevocado=None).all()
        serializer = self.serializer_class(graduados, many=True)
        return Response(serializer.data, HTTP_200_OK)

#TODO Falta proteger la ruta
#Solamente tendra acceso a solicitar y asignar el jefe de area.
class AsignarSolicitarTutores(CreateAPIView):
    permission_classes = [IsJefeArea]
    serializer_class = serializers.AsignarSolicitarTutorSerializer

    def create(self, request, graduado):
        area = self.request.user.area
        graduado = get_object_or_404(Graduado,pk=graduado,area=area)
        data = request.data
        data.setdefault('graduado',graduado)
        serializer = serializers.AsignarSolicitarTutorSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors,HTTP_400_BAD_REQUEST)

        result = serializer.create(serializer.validated_data)
        if 'tutores' in result:
            result['tutores'] = 'Tutores asignados correctamente'
        if 'areas_solicitadas' in result:
            result['areas_solicitadas'] = 'Tutores externos solicitados correctamente'

        return Response(result,HTTP_200_OK)

class SolicitudesTutorEnviadas(ListAPIView):
    permission_classes = [IsJefeArea]
    serializer_class = serializers.SolicitudTutorExternoSerializer
    def get_queryset(self):
        area = self.request.user.area
        query = SolicitudTutorExterno.objects.filter(graduado__area=area).order_by('-fechaCreado').all()
        return query

class SolicitudesTutorPendientes(ListAPIView):
    permission_classes = [IsJefeArea]
    serializer_class = serializers.SolicitudTutorExternoSerializer
    def get_queryset(self):
        area = self.request.user.area
        query = SolicitudTutorExterno.objects.filter(graduado__area=area,fechaRespuesta=None).order_by('-fechaCreado').all()
        return query

class SolicitudesTutorRecibidas(ListAPIView):
    permission_classes = [IsJefeArea]
    serializer_class = serializers.SolicitudTutorExternoSerializer
    def get_queryset(self):
        area = self.request.user.area
        query = SolicitudTutorExterno.objects.filter(area=area).order_by('-fechaCreado').all()
        return query

class ObtenerResponderSolicitudesTutor(RetrieveAPIView, CreateAPIView):
    permission_classes = [IsJefeArea]
    serializer_class = serializers.SolicitudTutorExternoSerializer
    lookup_url_kwarg = ('solicitudID')
    lookup_field = 'pk'

    def get_area(self):
        return self.request.user.area
    def get_queryset(self):
        area = self.get_area()
        query = SolicitudTutorExterno.objects.filter(Q(graduado__area=area)|Q(area=area),pk=self.kwargs['solicitudID'])
        return query
    def create(self, request,solicitudID):
        area = self.get_area()
        solicitud = get_object_or_404(SolicitudTutorExterno, area=area, pk=self.kwargs['solicitudID'])
        if solicitud.respuesta is not None:
            return Response({'detail': 'Solicitud respondida anteriormente'}, HTTP_400_BAD_REQUEST)
        data = request.data
        data['area']=area
        serializer = serializers.ResponderSolicitudSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors,HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        validated_data['solicitud'] = solicitud
        solicitud = serializer.create(validated_data)
        return Response({'detail':'Solicitud {resp} correctamente'.format(resp='aceptada' if solicitud.respuesta else 'rechazada')},HTTP_200_OK)

