from django.urls import path

# Create your views here.
from core.formacion_individual.base.views import ImportarGraduadosDirectorio, \
    ListGraduadosDelArea, ImportarTutoresDirectorio, ImportarEstudiantesDirectorio, ListEstudiantesDelArea, \
    ListJovenesDelArea

app_name = 'BaseFormacionComplementaria'

urlpatterns = [
    path('directorio/<int:areaID>/estudiante', ImportarEstudiantesDirectorio.as_view()),
    path('directorio/graduado', ImportarGraduadosDirectorio.as_view()),
    path('directorio/<int:areaID>/tutor', ImportarTutoresDirectorio.as_view()),

    path('area/<int:areaID>/estudiante', ListEstudiantesDelArea.as_view()),
    path('area/<int:areaID>/graduados', ListGraduadosDelArea.as_view()),
    path('area/<int:areaID>/jovenes', ListJovenesDelArea.as_view()),

]
