from django.urls import path

from core.formacion_complementaria.gestionar_avales.views import ObtenerGraduadosSinAval
from .views import ObtenerCrearActualizarAval
# Create your views here.
app_name = 'GestionarAval'
#TODO Avales no solo en Formación Complementaria
urlpatterns = [
    path('user/<int:usuario>/aval',ObtenerCrearActualizarAval.as_view()),
    path('graduado/sin-aval',ObtenerGraduadosSinAval.as_view()),
]