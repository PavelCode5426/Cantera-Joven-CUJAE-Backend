from django.urls import path
from rest_framework import routers

from core.familiarizacion.gestionar_area.views import ListarUbicacionesPosibleGraduado, \
    ListarObtenerPosibleGraduadoListAPIView, PreubicadosPorAreaListAPIView
from .views import ListarObtenerArea, ListarCrearPreubicacionLaboralAdelantadaAPIView, \
    AceptarRechazarUbicacionLaboralAdelantadaAPIView

# Create your views here.
app_name = 'GestionarArea'

router = routers.SimpleRouter()
router.register('area', ListarObtenerArea, 'Area')

urlpatterns = [
                  path('posible-graduado', ListarObtenerPosibleGraduadoListAPIView.as_view()),
                  path('posible-graduado/<int:posibleGraduado>/preubicacion-laboral',
                       ListarUbicacionesPosibleGraduado.as_view()),

                  path('preubicacion-laboral', ListarCrearPreubicacionLaboralAdelantadaAPIView.as_view()),
                  path('preubicacion-laboral/aceptar-rechazar',
                       AceptarRechazarUbicacionLaboralAdelantadaAPIView.as_view()),

                  path('area/<int:areaID>/posibles-graduados', PreubicadosPorAreaListAPIView.as_view()),

              ] + router.urls
