from django.urls import path
from . import views
from rest_framework import routers
# Create your views here.
app_name = 'cantera_listar_cantera'

router = routers.SimpleRouter()

urlpatterns = [
    path('estudiante/sin-aval',views.ListEstudiantesSinAval.as_view()),
    path('area/estudiantes',views.ListEstudiantesDelArea.as_view()),
    path('area/esttudiantes/sin-aval',views.ListEstudinatesDelAreaSinAval.as_view()),
]