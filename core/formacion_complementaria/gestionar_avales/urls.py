from django.urls import path
from .views import ObtenerCrearActualizarAval
# Create your views here.
app_name = 'GestionarAval'

urlpatterns = [
    path('user/<int:usuario>/aval',ObtenerCrearActualizarAval.as_view())
]