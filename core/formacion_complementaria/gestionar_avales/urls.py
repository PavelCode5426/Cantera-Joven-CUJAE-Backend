from django.urls import path

from core.formacion_complementaria.gestionar_avales.views import ObtenerGraduadosSinAval
from .views import ObtenerCrearActualizarAval

# Create your views here.
app_name = 'GestionarAval'

urlpatterns = [
    # TODO QUITAR LOS GRADUADOS SIN AVAL Y PONERLO EN UN FILTRO POR LOS GRADUADOS

    path('user/<int:usuario>/aval', ObtenerCrearActualizarAval.as_view()),
    path('graduado/sin-aval', ObtenerGraduadosSinAval.as_view()),
]
