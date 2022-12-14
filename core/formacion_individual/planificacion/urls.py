from django.urls import path

from core.formacion_individual.planificacion.views import CreateRetrieveGraduadoPFC, RetrieveUpdateEtapaFormacion, \
    EvaluarEtapaFormacion, ListEtapasPlanFormacion, ListPlanFormacionInArea, \
    ListPlanFormacionInTutor, ListCreatePlanFormacionCommets, EvaluarPlanFormacion, AprobarEvaluacion, \
    RetriveUpdatePlanFormacion, VersionesPlanFormacion, FirmarPlanFormacion, \
    ListCreateActividadFormacion, RetrieveUpdateDeleteActividadFormacion, ListCreateActividadFormacionCommets, \
    ExportarPDFPlanFormacionComplemtaria, ExportarCalendarioPlanFormacionComplemtaria, \
    SolicitarRevisionActividadFormacion, ListCreateSubActividadFormacion, RetrieveDeleteArchive, \
    ActividadFormacionUploadFile

app_name = 'PlanificacionFormacionIndividual'

urlpatterns = [
    path('joven/<int:jovenID>/plan', CreateRetrieveGraduadoPFC.as_view()),
    # ME TENDRA QUE DAR LOS PLANES DEL GRADUADO Y DEL ESTUDIANTE
    path('area/<int:areaID>/planes', ListPlanFormacionInArea.as_view()),
    # MUESTRA TAMBIEN LOS PLANES DEL GRADUADO Y EL ESTUDIANTE
    path('tutor/<int:tutorID>/planes', ListPlanFormacionInTutor.as_view()),

    path('plan/<int:planID>', RetriveUpdatePlanFormacion.as_view()),
    # OBTENER Y SOLAMENTE ACTUALIZAR LOS ESTADOS
    path('plan/<int:planID>/etapas', ListEtapasPlanFormacion.as_view()),
    path('plan/<int:planID>/comentarios', ListCreatePlanFormacionCommets.as_view()),
    path('plan/<int:planID>/evaluar', EvaluarPlanFormacion.as_view()),  # SOLO PARA PLANES DE FORMACION
    path('plan/<int:planID>/versiones', VersionesPlanFormacion.as_view()),
    path('plan/<int:planID>/firmar', FirmarPlanFormacion.as_view()),  # PERMITE APROBAR O RECHAZAR EL PLAN
    path('plan/<int:planID>/export-pdf', ExportarPDFPlanFormacionComplemtaria.as_view()),
    path('plan/<int:planID>/export-calendar', ExportarCalendarioPlanFormacionComplemtaria.as_view()),

    path('etapa/<int:etapaID>', RetrieveUpdateEtapaFormacion.as_view()),
    path('etapa/<int:etapaID>/actividades', ListCreateActividadFormacion.as_view()),  # CREAR Y LISTAR TAREAS
    path('etapa/<int:etapaID>/evaluar', EvaluarEtapaFormacion.as_view()),
    path('actividad/<int:actividadID>', RetrieveUpdateDeleteActividadFormacion.as_view()),

    # OBTENER TAREA, BORRAR , ACTUALIZAR Y ACTUALIZAR PARA CAMBIAR DE ESTADO (SOLO TUTOR)
    path('actividad/<int:actividadID>/solicitar-revision', SolicitarRevisionActividadFormacion.as_view()),

    # PERMITE AL JOVEN SOLICITAR REVISION DE LA TAREA
    path('actividad/<int:actividadID>/comentarios', ListCreateActividadFormacionCommets.as_view()),
    path('actividad/<int:actividadID>/subactividades', ListCreateSubActividadFormacion.as_view()),
    path('actividad/<int:actividadID>/subir-archivo', ActividadFormacionUploadFile.as_view()),
    path('archivo/<int:archivoID>', RetrieveDeleteArchive.as_view()),

    # TODO COMPLETAR LAS EVALUACIONES
    path('evaluacion/<int:evaluacionID>/aprobar', AprobarEvaluacion.as_view()),
]

# TODO FALTA FORZAR CIERRE DEL PLAN DE FORMACION QUE SE HIZO MEDIANTE LAS EVALUACIONES
