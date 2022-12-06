from django.urls import path

# Create your views here.
from core.formacion_complementaria.planificacion.views import CreateRetrieveGraduadoPFC, RetrieveUpdateEtapaFormacion, \
    EvaluarEtapaFormacion, ListEtapasPlanFormacionComplementaria, ListPlanFormacionComplementariaInArea, \
    ListPlanFormacionComplementariaInTutor

app_name = 'PlanificacionFormacionComplementaria'

urlpatterns = [
    path('graduado/<int:graduadoID>/plan', CreateRetrieveGraduadoPFC.as_view()),

    path('area/<int:areaID>/planes', ListPlanFormacionComplementariaInArea.as_view()),
    path('tutor/<int:tutorID>/planes', ListPlanFormacionComplementariaInTutor.as_view()),

    path('plan/<planID>/etapas', ListEtapasPlanFormacionComplementaria.as_view()),
    path('etapa/<int:etapaID>', RetrieveUpdateEtapaFormacion.as_view()),
    path('etapa/<int:etapaID>/evaluar', EvaluarEtapaFormacion.as_view()),
]
