from django.urls import path
from rest_framework import routers

from core.familiarizacion.gestionar_area.views import ListarUbicacionesPosibleGraduado
from .views import ListarObtenerArea, ListarCrearPreubicacionLaboralAdelantadaAPIView, \
    AceptarRechazarUbicacionLaboralAdelantadaAPIView, ListarObtenerPosibleGraduadoGenericViewSet, \
    ListarPosibleGraduadoNoPreubicadoAPIView

# Create your views here.
app_name = 'GestionarArea'

router = routers.SimpleRouter()
router.register('area', ListarObtenerArea, 'Area')
router.register('posible-graduado', ListarObtenerPosibleGraduadoGenericViewSet, 'Posible-Graduado')

# TODO SI TE DAS CUENTA AQUI ESTAMOS DANDO LOS POSIBLES GRADUADOS ARRIBA. A LO MEJOR ES CONVENIENTE
# CAMBIAR LAS COSAS Y FILTRAR O CREAR UNA URL CUSTOM PARA FILTRAR SOLAMENTE LA PREUBICACION
# VALORARLO

urlpatterns = [
                  path('posible-graduado/no-preubicado', ListarPosibleGraduadoNoPreubicadoAPIView.as_view()),
                  path('posible-graduado/<int:posibleGraduado>/pre-ubicacion',
                       ListarUbicacionesPosibleGraduado.as_view()),

                  path('area/preubicacion', ListarCrearPreubicacionLaboralAdelantadaAPIView.as_view()),
                  path('area/preubicacion/aceptar-rechazar',
                       AceptarRechazarUbicacionLaboralAdelantadaAPIView.as_view()),
              ] + router.urls
