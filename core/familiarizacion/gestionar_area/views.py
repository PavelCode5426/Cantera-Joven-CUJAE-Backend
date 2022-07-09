from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from core.base.helpers import notificar_al_DRH
from . import serializers
from core.base.models import modelosSimple,modelosPlanificacionFamiliarizarcion,modelosUsuario
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from core.base.permissions import IsJefeArea, IsVicerrector, IsDirectorRH


class ListarObtenerArea(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    #permission_classes = [IsDirectorRH, IsVicerrector]
    serializer_class = serializers.AreaSerializer
    queryset = modelosSimple.Area.objects.all()

class ListarCrearPreubicacionLaboralAdelantadaAPIView(ListCreateAPIView):
    #permission_classes = [IsDirectorRH, IsVicerrector, IsJefeArea]
    queryset = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.objects.filter(esPreubicacion=True).all()
    serializer_class = serializers.PreubicacionLaboralAdelantadaSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data,many=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response({'detail':'Preubicacion Laboral Realizada Correctamente'},HTTP_200_OK)
        return Response(serializer.errors,HTTP_400_BAD_REQUEST)

    def list(self, request):
        data = list()
        areas = modelosSimple.Area.objects.all()
        for area in areas:
            posiblesGraduados = modelosUsuario.PosibleGraduado.objects.filter(ubicacionlaboraladelantada__area=area,ubicacionlaboraladelantada__esPreubicacion=True).all()
            data.append({
                'area':serializers.AreaSerializer(area).data,
                'ubicados':serializers.PosibleGraduadoSerializer(posiblesGraduados,many=True).data
            })

        return Response(data,HTTP_200_OK)

class AceptarRechazarUbicacionLaboralAdelantadaAPIView(APIView):
    #permission_classes = [IsVicerrector]
    serializer_class = serializers.SendNotificationSerializer
    def post(self,request):
        serializador = self.serializer_class(data=request.data)
        if not serializador.is_valid():
            return Response(serializador.errors,HTTP_400_BAD_REQUEST)

        response = None
        aceptada = serializador.validated_data.get('aceptada')
        notificacion = serializador.validated_data.get('mensaje')

        if notificacion:
            notificar_al_DRH(notificacion)

        if aceptada:
            preubicaciones=modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.objects.filter(esPreubicacion=True)
            for preubicacion in preubicaciones:
                preubicacion.esPreubicacion = False
            modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.objects.bulk_update(preubicaciones,['esPreubicacion'])

            response = Response({'detail':'Ubicacion Laboral Adelantada Aceptada'},HTTP_200_OK)
        else:
            response = Response({'detail':'Ubicacion Laboral Adelantada Rechazada'},HTTP_200_OK)

        return response

class ListarObtenerPosibleGraduadoGenericViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    serializer_class = serializers.PosibleGraduadoSerializer
    queryset = modelosUsuario.PosibleGraduado.objects.all()

class ListarPosibleGraduadoNoPreubicadoAPIView(ListAPIView):
    serializer_class = serializers.PosibleGraduadoSerializer
    queryset = modelosUsuario.PosibleGraduado.objects.filter(ubicacionlaboraladelantada=None).all()

class ListarUbicacionesPosibleGraduado(ListAPIView):
    serializer_class = serializers.PreubicacionLaboralAdelantadaModelSerializer

    def list(self, request,posibleGraduado):
        posibleGraduado = get_object_or_404(modelosUsuario.PosibleGraduado,pk=posibleGraduado)
        ubicaciones = posibleGraduado.ubicacionlaboraladelantada_set.all()

        data = self.get_serializer(ubicaciones,many=True).data
        return Response(data,HTTP_200_OK)


