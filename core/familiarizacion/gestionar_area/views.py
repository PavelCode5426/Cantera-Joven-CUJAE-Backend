from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from core.base.helpers import notificar_al_DRH
from .serializers import AreaSerializer,PreubicacionLaboralAdelantadaSerializer,SendNotificationSerializer
from core.base.models import modelosSimple,modelosPlanificacionFamiliarizarcion
from rest_framework.viewsets import mixins,GenericViewSet
from rest_framework.generics import ListCreateAPIView

class ListarObtenerArea(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    serializer_class = AreaSerializer
    queryset = modelosSimple.Area.objects.all()


class ListarCrearPreubicacionLaboralAdelantada(ListCreateAPIView):
    serializer_class = PreubicacionLaboralAdelantadaSerializer
    queryset = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.objects.filter(esPreubicacion=True)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,many=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response({'detail':'Preubicacion Laboral Realizada Correctamente'},HTTP_200_OK)

        return Response(serializer.errors,HTTP_400_BAD_REQUEST)


class AceptarRechazarUbicacionLaboralAdelantada(APIView):
    serializer_class = SendNotificationSerializer
    def post(self,request,*args,**kwargs):
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




