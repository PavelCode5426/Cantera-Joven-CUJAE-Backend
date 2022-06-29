from django.urls import path
# Create your views here.
from .views import PosiblesGraduadosEnDirectorio,PosibleGraduadoEnDirectorio


app_name = 'BaseFamiliarizacion'

urlpatterns = [
    path('directorio/posible-graduado',PosiblesGraduadosEnDirectorio.as_view()),
    path('directorio/posible-graduado/<int:posibleGraduadoID>',PosibleGraduadoEnDirectorio.as_view()),
]