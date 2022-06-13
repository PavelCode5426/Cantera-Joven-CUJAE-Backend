from django.urls import path
# Create your views here.
from .views import EstudiantesEnDirectorio,EstudianteEnDirectorio

app_name = 'BaseCantera'

urlpatterns = [
    path('directorio/estudiante',EstudiantesEnDirectorio.as_view()),
    path('directorio/estudiante/<int:estudianteID>',EstudianteEnDirectorio.as_view()),
]


