from django.urls import path

# Create your views here.
from .views import PosiblesGraduadosEnDirectorio, PosibleGraduadoEnDirectorio

app_name = 'BaseFamiliarizacion'

urlpatterns = [
    # TODO HACER LO MISMO QUE EN EL ESTUDIANTE. HAY QUE HABLAR CON PICAYO
    path('directorio/posible-graduado', PosiblesGraduadosEnDirectorio.as_view()),
    path('directorio/posible-graduado/<int:posibleGraduadoID>', PosibleGraduadoEnDirectorio.as_view()),
]
