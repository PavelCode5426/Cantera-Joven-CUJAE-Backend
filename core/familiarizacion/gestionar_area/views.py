from rest_framework.generics import ListCreateAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import mixins, GenericViewSet

from core.base.helpers import notificar_al_DRH
from core.base.models import modelosSimple, modelosPlanificacionFamiliarizarcion, modelosUsuario
from . import serializers
from .filters import PosibleGraduadoPreubicadoFilterSet
from ...base.models.modelosUsuario import PosibleGraduado
from ...base.permissions import IsDirectorRecursosHumanos, IsJefeArea, IsVicerrector, IsSameAreaPermissions, \
    IsSameUserWhoRequestPermissions, IsPosibleGraduado


class ListarObtenerArea(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = serializers.AreaSerializer
    queryset = modelosSimple.Area.objects.all()


class ListarCrearPreubicacionLaboralAdelantadaAPIView(ListCreateAPIView):
    permission_classes = [IsDirectorRecursosHumanos]
    serializer_class = serializers.PreubicacionLaboralAdelantadaSerializer

    def get_queryset(self):
        return modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.objects.filter(esPreubicacion=True).all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response({'detail': 'Preubicacion Laboral Realizada Correctamente'}, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)

    def list(self, request):
        # TODO OPTIMIZAR LAS CONSULTAS
        data = list()
        areas = modelosSimple.Area.objects.all()
        for area in areas:
            posiblesGraduados = modelosUsuario.PosibleGraduado \
                .objects.filter(ubicacionlaboraladelantada__area=area,
                                ubicacionlaboraladelantada__esPreubicacion=True,
                                evaluacion=None
                                ).all()
            data.append({
                'area': serializers.AreaSerializer(area).data,
                'ubicados': serializers.PosibleGraduadoSerializer(posiblesGraduados, many=True).data
            })

        return Response(data, HTTP_200_OK)


class AceptarRechazarUbicacionLaboralAdelantadaAPIView(APIView):
    permission_classes = [IsVicerrector]
    serializer_class = serializers.SendNotificationSerializer

    def post(self, request):
        serializador = self.serializer_class(data=request.data)
        if not serializador.is_valid():
            return Response(serializador.errors, HTTP_400_BAD_REQUEST)

        aceptada = serializador.validated_data.get('aceptada')
        notificacion = serializador.validated_data.get('mensaje')

        if notificacion:
            notificar_al_DRH(notificacion)

        if aceptada:
            preubicaciones = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.objects.filter(
                esPreubicacion=True)
            for preubicacion in preubicaciones:
                preubicacion.esPreubicacion = False
            modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.objects.bulk_update(preubicaciones,
                                                                                                ['esPreubicacion'])

            response = Response({'detail': 'Ubicacion Laboral Adelantada Aceptada'}, HTTP_200_OK)
        else:
            response = Response({'detail': 'Ubicacion Laboral Adelantada Rechazada'}, HTTP_200_OK)

        return response


class ListarObtenerPosibleGraduadoListAPIView(ListAPIView):
    """ Permite listar y filtrar los posibles graduados si están ubicados o no laboralmente. Esta interfaz solamente sera
        accesible para los jefes de area y el director de recursos humanos. """

    permission_classes = [IsDirectorRecursosHumanos]
    serializer_class = serializers.PosibleGraduadoSerializer
    filterset_class = PosibleGraduadoPreubicadoFilterSet

    def get_queryset(self):
        return PosibleGraduado.objects.filter(evaluacion=None).all()


class ListarUbicacionesPosibleGraduado(ListAPIView):
    permission_classes = [
        IsDirectorRecursosHumanos |
        IsSameUserWhoRequestPermissions, IsPosibleGraduado |
        IsSameAreaPermissions, IsJefeArea
    ]
    serializer_class = serializers.PreubicacionLaboralAdelantadaModelSerializer

    def get_queryset(self):
        posibleGraduado = get_object_or_404(modelosUsuario.PosibleGraduado, pk=self.kwargs['posibleGraduado'])
        ubicaciones = posibleGraduado.ubicacionlaboraladelantada_set.all()
        return ubicaciones

    # def list(self, request):
    #     data = self.get_serializer(self.get_queryset(), many=True).data
    #     return Response(data, HTTP_200_OK)


class PreubicadosPorAreaListAPIView(ListAPIView):
    """ Permite listar y filtrar los posibles graduados si están ubicados a un area. Esta interfaz solamente sera
        accesible para los jefes de area y el director de recursos humanos. Permisos para que el jefe de area que
        vea el area de la que el es el jefe """

    permission_classes = [IsVicerrector | IsDirectorRecursosHumanos | IsSameAreaPermissions, IsJefeArea]
    serializer_class = serializers.PosibleGraduadoSerializer
    filterset_class = PosibleGraduadoPreubicadoFilterSet

    def get_queryset(self):
        areaID = self.kwargs['areaID']
        # MUESTRA LOS YA UBICADOS EN EL AREA
        return PosibleGraduado.objects.filter(ubicacionlaboraladelantada__area_id=areaID,
                                              ubicacionlaboraladelantada__esPreubicacion=False).all()
