from django.urls import path

# Create your views here.
from core.formacion_complementaria.base.views import GraduadosEnDirectorio, ObtenerGraduadoEnDirectorio

app_name = 'BaseFormacionComplementaria'

urlpatterns = [
    # TODO IDENTICO QUE EN EL ESTUDIANTE
    path('directorio/graduado', GraduadosEnDirectorio.as_view()),
    path('directorio/graduado/<int:graduadoID>', ObtenerGraduadoEnDirectorio.as_view()),
]
