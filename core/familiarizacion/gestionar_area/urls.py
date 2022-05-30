from django.urls import path
from rest_framework import routers

from .views import ListarObtenerArea,ListarCrearPreubicacionLaboralAdelantada,AceptarRechazarUbicacionLaboralAdelantada

# Create your views here.
app_name = 'GestionarArea'

router = routers.SimpleRouter()
router.register('area',ListarObtenerArea,'Area')

urlpatterns = router.urls + [
    path('area/preubicacion',ListarCrearPreubicacionLaboralAdelantada.as_view()),
    path('area/preubicacion/aceptar-rechazar',AceptarRechazarUbicacionLaboralAdelantada.as_view()),
]