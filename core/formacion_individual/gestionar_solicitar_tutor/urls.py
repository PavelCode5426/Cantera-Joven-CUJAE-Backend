from django.urls import path
from rest_framework import routers

from . import views

# Create your views here.
app_name = 'GestionarSolicitarTutor'

router = routers.SimpleRouter()

urlpatterns = [

                  path('area/<int:areaID>/tutores', views.TutoresPorAreaListAPIView.as_view()),
                  path('joven/<int:jovenID>/tutores', views.TutoresPorGraduadoListAPIView.as_view()),
                  path('tutor/<int:tutorID>/tutorados', views.TutoradosPorTutorListAPIView.as_view()),

                  # Solicitudes de Tutor
                  path('joven/<int:jovenID>/asignar-solicitar', views.AsignarSolicitarTutores.as_view()),
                  path('area/<int:areaID>/solicitud-tutor', views.SolicitudesTutorListAPIView.as_view()),
                  path('solicitud-tutor/<int:solicitudID>', views.ObtenerResponderSolicitudesTutor.as_view()),

              ] + router.urls
