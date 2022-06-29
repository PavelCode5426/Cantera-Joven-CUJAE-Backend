from django.urls import path
from rest_framework import routers

from core.familiarizacion.gestionar_area.views import ListarUbicacionesPosibleGraduado
from .views import ListarObtenerArea,ListarCrearPreubicacionLaboralAdelantadaAPIView,AceptarRechazarUbicacionLaboralAdelantadaAPIView,ListarObtenerPosibleGraduadoGenericViewSet,ListarPosibleGraduadoNoPreubicadoAPIView

# Create your views here.
app_name = 'GestionarArea'

router = routers.SimpleRouter()
router.register('area', ListarObtenerArea, 'Area')
router.register('posible-graduado', ListarObtenerPosibleGraduadoGenericViewSet, 'Posible-Graduado')

urlpatterns = [
    path('posible-graduado/no-preubicado',ListarPosibleGraduadoNoPreubicadoAPIView.as_view()),
    path('posible-graduado/<int:posibleGraduado>/pre-ubicacion',ListarUbicacionesPosibleGraduado.as_view()),

    path('area/preubicacion', ListarCrearPreubicacionLaboralAdelantadaAPIView.as_view()),
    path('area/preubicacion/aceptar-rechazar', AceptarRechazarUbicacionLaboralAdelantadaAPIView.as_view()),
] + router.urls