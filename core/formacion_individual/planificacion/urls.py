from django.urls import path
from rest_framework.routers import DefaultRouter

from core.formacion_individual.planificacion.views import CreateRetrieveJovenPlanFormacion, \
    RetrieveUpdateEtapaFormacion, \
    EvaluarEtapaFormacion, ListEtapasPlanFormacion, ListPlanFormacionInArea, \
    ListPlanFormacionInTutor, ListCreatePlanFormacionCommets, EvaluarPlanFormacion, AprobarEvaluacion, \
    RetriveUpdatePlanFormacion, VersionesPlanFormacion, FirmarPlanFormacion, \
    ListCreateActividadFormacion, RetrieveUpdateDeleteActividadFormacion, ListCreateActividadFormacionCommets, \
    ExportarPDFPlanFormacionComplemtaria, ExportarCalendarioPlanFormacionComplemtaria, \
    SolicitarRevisionActividadFormacion, ListCreateSubActividadFormacion, RetrieveDeleteArchive, \
    ActividadFormacionUploadFile, ListRetrieveEvaluacionesArea, PropuestaMovimientoModelViewset

app_name = 'PlanificacionFormacionIndividual'

urlpatterns = [
    path('joven/<int:jovenID>/plan-individual', CreateRetrieveJovenPlanFormacion.as_view()),
    # ME TENDRA QUE DAR LOS PLANES DEL GRADUADO Y DEL ESTUDIANTE
    path('area/<int:areaID>/planes', ListPlanFormacionInArea.as_view()),
    # MUESTRA TAMBIEN LOS PLANES DEL GRADUADO Y EL ESTUDIANTE
    path('tutor/<int:tutorID>/planes', ListPlanFormacionInTutor.as_view()),

    path('plan-individual/<int:planID>', RetriveUpdatePlanFormacion.as_view()),
    # OBTENER Y SOLAMENTE ACTUALIZAR LOS ESTADOS
    path('plan-individual/<int:planID>/etapas', ListEtapasPlanFormacion.as_view()),
    path('plan-individual/<int:planID>/comentarios', ListCreatePlanFormacionCommets.as_view()),
    path('plan-individual/<int:planID>/evaluar', EvaluarPlanFormacion.as_view()),  # SOLO PARA PLANES DE FORMACION
    path('plan-individual/<int:planID>/versiones', VersionesPlanFormacion.as_view()),
    path('plan-individual/<int:planID>/firmar', FirmarPlanFormacion.as_view()),  # PERMITE APROBAR O RECHAZAR EL PLAN
    path('plan-individual/<int:planID>/export-pdf', ExportarPDFPlanFormacionComplemtaria.as_view()),
    path('plan-individual/<int:planID>/export-calendar', ExportarCalendarioPlanFormacionComplemtaria.as_view()),

    path('etapa-formacion/<int:etapaID>', RetrieveUpdateEtapaFormacion.as_view()),
    path('etapa-formacion/<int:etapaID>/actividades', ListCreateActividadFormacion.as_view()),  # CREAR Y LISTAR TAREAS
    path('etapa-formacion/<int:etapaID>/evaluar', EvaluarEtapaFormacion.as_view()),
    path('actividad-formacion/<int:actividadID>', RetrieveUpdateDeleteActividadFormacion.as_view()),

    # OBTENER TAREA, BORRAR , ACTUALIZAR Y ACTUALIZAR PARA CAMBIAR DE ESTADO (SOLO TUTOR)
    path('actividad-formacion/<int:actividadID>/solicitar-revision', SolicitarRevisionActividadFormacion.as_view()),

    # PERMITE AL JOVEN SOLICITAR REVISION DE LA TAREA
    path('actividad-formacion/<int:actividadID>/comentarios', ListCreateActividadFormacionCommets.as_view()),
    path('actividad-formacion/<int:actividadID>/subactividades', ListCreateSubActividadFormacion.as_view()),
    path('actividad-formacion/<int:actividadID>/subir-archivo', ActividadFormacionUploadFile.as_view()),
    # path('archivo/<int:archivoID>', RetrieveDeleteArchive.as_view()),

    path('evaluacion-formacion/<int:evaluacionID>/aprobar', AprobarEvaluacion.as_view()),
]

router = DefaultRouter()
router.register('evaluacion', ListRetrieveEvaluacionesArea, 'area-evaluaciones')
router.register('propuesta-moviemiento', PropuestaMovimientoModelViewset, 'propuesta-movimiento')
router.register('archivo', RetrieveDeleteArchive, 'archivo')

urlpatterns += router.urls
