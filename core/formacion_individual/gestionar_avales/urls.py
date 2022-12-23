from django.urls import path
from rest_framework import routers

from .views import ObtenerCrearActualizarAval, PlantillaAvalModelViewSet

# Create your views here.
app_name = 'GestionarAval'

router = routers.SimpleRouter()
router.register('plantilla-aval', PlantillaAvalModelViewSet, 'PlantillaAval')

urlpatterns = [
                  path('user/<int:usuarioID>/aval', ObtenerCrearActualizarAval.as_view()),
              ] + router.get_urls()
