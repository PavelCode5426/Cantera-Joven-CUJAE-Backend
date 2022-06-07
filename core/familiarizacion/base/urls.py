from django.urls import path
# Create your views here.
from .views import EstudiantesEnDirectorio,EstudianteEnDirectorio,PosiblesGraduadosEnDirectorio,PosibleGraduadoEnDirectorio

app_name = 'BaseFamiliarizacion'

urlpatterns = [
    path('directorio/estudiante',EstudiantesEnDirectorio.as_view()),
    path('directorio/estudiante/<int:estudianteID>',EstudianteEnDirectorio.as_view()),

    path('directorio/posible-graduado',PosiblesGraduadosEnDirectorio.as_view()),
    path('directorio/posible-graduado/<int:posibleGraduadoID>',PosibleGraduadoEnDirectorio.as_view()),
]