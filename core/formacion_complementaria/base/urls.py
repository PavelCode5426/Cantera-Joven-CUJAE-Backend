from django.urls import path

# Create your views here.
from core.formacion_complementaria.base.views import ImportarGraduadosDirectorio, \
    ListGraduadosDelArea, ImportarTutoresDirectorio

app_name = 'BaseFormacionComplementaria'

urlpatterns = [
    path('directorio/graduado', ImportarGraduadosDirectorio.as_view()),
    path('directorio/<int:areaID>/tutor', ImportarTutoresDirectorio.as_view()),

    # OBTIENE TODOS LOS GRADUADOS DEL AREA
    path('area/<int:areaID>/graduados', ListGraduadosDelArea.as_view()),
]
