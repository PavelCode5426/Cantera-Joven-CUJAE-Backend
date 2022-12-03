from django.urls import path

# Create your views here.
from .views import ImportarEstudiantesDirectorio, ListEstudiantesDelArea

app_name = 'BaseCantera'

urlpatterns = [
    path('directorio/<int:areaID>/estudiante', ImportarEstudiantesDirectorio.as_view()),

    path('area/<int:areaID>/estudiante', ListEstudiantesDelArea.as_view())
]
