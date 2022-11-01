from django.urls import path
from rest_framework import routers

from . import views

# Create your views here.
app_name = 'cantera_listar_cantera'

router = routers.SimpleRouter()

urlpatterns = [

    # TODO RECOMIENDO UNIR TODO ESTO EN UN SOLO ENDPOINT

    path('estudiante/sin-aval', views.ListEstudiantesSinAval.as_view()),
    path('area/estudiantes', views.ListEstudiantesDelArea.as_view()),
    path('area/estudiantes/sin-aval', views.ListEstudinatesDelAreaSinAval.as_view()),
]
