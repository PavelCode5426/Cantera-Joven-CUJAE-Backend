from django.urls import path
from rest_framework.views import APIView

from core.formacion_complementaria.planificacion.views import CreateRetrieveGraduadoPFC, RetrieveUpdateEtapaFormacion, \
    EvaluarEtapaFormacion, ListEtapasPlanFormacionComplementaria, ListPlanFormacionComplementariaInArea, \
    ListPlanFormacionComplementariaInTutor, ListCreatePlanFormacionCommets, EvaluarPlanFormacion, AprobarEvaluacion, \
    RetriveUpdatePlanFormacionComplementaria, VersionesPlanFormacionComplementaria, FirmarPlanFormacionComplementaria, \
    ListCreateActividadFormacion, RetrieveUpdateDeleteActividadFormacion, ListCreateActividadFormacionCommets, \
    ExportarPDFPlanFormacionComplemtaria, ExportarCalendarioPlanFormacionComplemtaria

app_name = 'PlanificacionFormacionComplementaria'

urlpatterns = [
    path('graduado/<int:graduadoID>/plan', CreateRetrieveGraduadoPFC.as_view()),
    # TODO CAMBIAR ESTO PARA QUE SEA GENERAL
    # ME TENDRA QUE DAR LOS PLANES DEL GRADUADO Y DEL ESTUDIANTE
    path('area/<int:areaID>/planes', ListPlanFormacionComplementariaInArea.as_view()),
    # MUESTRA TAMBIEN LOS PLANES DEL GRADUADO Y EL ESTUDIANTE
    path('tutor/<int:tutorID>/planes', ListPlanFormacionComplementariaInTutor.as_view()),

    path('plan/<int:planID>', RetriveUpdatePlanFormacionComplementaria.as_view()),
    # OBTENER Y SOLAMENTE ACTUALIZAR LOS ESTADOS
    path('plan/<int:planID>/etapas', ListEtapasPlanFormacionComplementaria.as_view()),
    path('plan/<int:planID>/comentarios', ListCreatePlanFormacionCommets.as_view()),
    path('plan/<int:planID>/evaluar', EvaluarPlanFormacion.as_view()),  # SOLO PARA PLANES DE FORMACION
    path('plan/<int:planID>/versiones', VersionesPlanFormacionComplementaria.as_view()),
    path('plan/<int:planID>/firmar', FirmarPlanFormacionComplementaria.as_view()),  # PERMITE APROBAR O RECHAZAR EL PLAN
    path('plan/<int:planID>/export-pdf', ExportarPDFPlanFormacionComplemtaria.as_view()),
    path('plan/<int:planID>/export-calendar', ExportarCalendarioPlanFormacionComplemtaria.as_view()),

    path('etapa/<int:etapaID>', RetrieveUpdateEtapaFormacion.as_view()),
    path('etapa/<int:etapaID>/actividad', ListCreateActividadFormacion.as_view()),  # CREAR Y LISTAR TAREAS
    path('etapa/<int:etapaID>/evaluar', EvaluarEtapaFormacion.as_view()),

    path('actividad/<int:actividadID>', RetrieveUpdateDeleteActividadFormacion.as_view()),
    # OBTENER TAREA, BORRAR , ACTUALIZAR Y ACTUALIZAR PARA CAMBIAR DE ESTADO (SOLO GRADUADO)
    path('actividad/<int:actividadID>/comentarios', ListCreateActividadFormacionCommets.as_view()),
    path('actividad/<int:actividadID>/subtareas', APIView.as_view()),  # TODO OBTENER Y CREAR SUBTAREA

    path('evaluacion/<int:evaluacionID>/aprobar', AprobarEvaluacion.as_view()),
]

# TODO FALTA FORZAR CIERRE DEL PLAN DE FORMACION QUE SE HIZO MEDIANTE LAS EVALUACIONES
