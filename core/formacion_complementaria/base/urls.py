from django.urls import path

# Create your views here.
from core.formacion_complementaria.base.views import GraduadosEnDirectorio, \
    ListGraduadosDelArea

app_name = 'BaseFormacionComplementaria'

urlpatterns = [
    path('directorio/graduado', GraduadosEnDirectorio.as_view()),
    path('directorio/graduado/<int:graduadoID>', GraduadosEnDirectorio.as_view()),

    # OBTIENE TODOS LOS GRADUADOS DEL AREA
    path('area/<int:areaID>/graduados', ListGraduadosDelArea.as_view()),
]
