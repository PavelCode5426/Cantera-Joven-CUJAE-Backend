from django.urls import path
from rest_framework.routers import DefaultRouter

from core.formacion_colectiva.planificacion.views import ListCreateRetrieveUpdatePlanFormacionColectivo, \
    ListEtapasPlanFormacionColectivo, RetrieveUpdateEtapaPlanFormacionColectivo, ListCreatePlanColectivoCommets, \
    ListCreateActividadColectiva, RetrieveDeleteUpdateActividadColectiva, RetrieveJovenPlanColectivo, \
    FirmarPlanColectivo, ActividadColectivaUploadFile, ListCreateActividadArea, RetrieveDeleteArchive, \
    RetrieveDeleteUpdateActividadArea, ListAsistenciaActividad, ListJovenAsistencias, ExportarPlanColectivoPDF, \
    RetrieveCreateJovenEvaluacion, CerrarPlanColectivo

app_name = 'PlanificacionFormacionColectiva'

urlpatterns = [
    path('joven/<int:jovenID>/plan-colectivo', RetrieveJovenPlanColectivo.as_view()),
    path('joven/<int:jovenID>/asistencias', ListJovenAsistencias.as_view()),
    path('joven/<int:jovenID>/evaluacion', RetrieveCreateJovenEvaluacion.as_view()),

    path('plan-colectivo/<int:planID>/etapas', ListEtapasPlanFormacionColectivo.as_view()),
    path('plan-colectivo/<int:planID>/comentarios', ListCreatePlanColectivoCommets.as_view()),
    path('etapa/<int:etapaID>/actividades', ListCreateActividadColectiva.as_view()),
    path('plan-colectivo/<int:planID>/firmar', FirmarPlanColectivo.as_view()),
    path('plan-colectivo/<int:planID>/cerrar', CerrarPlanColectivo.as_view()),
    path('actividad-colectiva/<int:actividadID>/subir-archivo', ActividadColectivaUploadFile.as_view()),
    path('actividad-colectiva/<int:actividadID>/actividades-area', ListCreateActividadArea.as_view()),
    path('actividad/<int:actividadID>/asistencia', ListAsistenciaActividad.as_view()),
    path('plan-colectivo/<int:planID>/exportar-pdf', ExportarPlanColectivoPDF.as_view()),
]

router = DefaultRouter()
router.register('plan-colectivo', ListCreateRetrieveUpdatePlanFormacionColectivo, 'plan-colectivo')
router.register('etapa', RetrieveUpdateEtapaPlanFormacionColectivo, 'etapa-colectiva')
router.register('actividad-colectiva', RetrieveDeleteUpdateActividadColectiva, 'actividad-colectiva')
router.register('actividad-area', RetrieveDeleteUpdateActividadArea, 'actividad-area')
router.register('archivo', RetrieveDeleteArchive, 'archivo')

urlpatterns += router.urls
