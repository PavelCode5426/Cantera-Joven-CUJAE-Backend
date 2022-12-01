from django.urls import path

# Create your views here.
from .views import ImportarPosiblesGraduadosDirectorio

app_name = 'BaseFamiliarizacion'

urlpatterns = [
    path('directorio/posible-graduado', ImportarPosiblesGraduadosDirectorio.as_view()),
]
