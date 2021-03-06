from django.urls import path
from . import views
from rest_framework import routers
# Create your views here.
app_name = 'GestionarSolicitarTutor'

router = routers.SimpleRouter()

urlpatterns = [
    path('area/tutores',views.ListTutoresArea.as_view()),
    path('area/graduados',views.ListGraduadosDelArea.as_view()),
    path('area/graduados/sin-tutor',views.ListGraduadosSinTutor.as_view()),
    path('area/graduados/sin-aval',views.ListGraduadosDelAreaSinAval.as_view()),
    path('area/<int:areaID>/graduados/sin-aval',views.ListGraduadosDelAreaSinAval.as_view()),

    path('graduados/sin-aval',views.ListGraduadosSinAval.as_view()),

    path('graduado/tutores', views.ListTutoresGraduado.as_view()),
    path('graduado/<int:graduado>/tutores', views.ListTutoresGraduado.as_view()),
    path('graduado/<int:graduado>/asignar-solicitar',views.AsignarSolicitarTutores.as_view()),

    path('tutor/tutorados',views.ListGraduadosTutor.as_view()),
    path('tutor/<int:tutor>/tutorados',views.ListGraduadosTutor.as_view()),

    #Solicitudes de Tutor

    path('solicitud-tutor', views.SolicitudesTutorRecibidas.as_view()),
    path('solicitud-tutor/<int:solicitudID>', views.ObtenerResponderSolicitudesTutor.as_view()),
    path('solicitud-tutor/enviadas',views.SolicitudesTutorEnviadas.as_view()),
    path('solicitud-tutor/pendientes',views.SolicitudesTutorPendientes.as_view()),


] + router.urls