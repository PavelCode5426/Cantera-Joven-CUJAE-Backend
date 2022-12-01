from django.urls import path

# Create your views here.
from .views import ImportarEstudiantesDirectorio

app_name = 'BaseCantera'

urlpatterns = [
    path('directorio/<int:areaID>/estudiante', ImportarEstudiantesDirectorio.as_view()),
]
