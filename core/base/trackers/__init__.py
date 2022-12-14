from core.base import models
from custom.authentication import models as authModels
from custom.logging.tracker import modelTracker


def registerModels():
    modelTracker.register(authModels.DirectoryUserAPIKey)

    modelTracker.register(models.modelosUsuario.Estudiante)
    modelTracker.register(models.modelosUsuario.Graduado)
    modelTracker.register(models.modelosUsuario.PosibleGraduado)
    modelTracker.register(models.modelosUsuario.Aval)

    modelTracker.register(models.modelosSimple.Configuracion)
    modelTracker.register(models.modelosSimple.PropuestaMovimiento)
    modelTracker.register(models.modelosSimple.Dimension)

    modelTracker.register(models.modelosTutoria.SolicitudTutorExterno)
    modelTracker.register(models.modelosTutoria.TutoresAsignados)

    modelTracker.register(models.modelosPlanificacion.Plan)
    modelTracker.register(models.modelosPlanificacion.Etapa)
    modelTracker.register(models.modelosPlanificacion.Comentario)
    modelTracker.register(models.modelosPlanificacion.Evaluacion)
    modelTracker.register(models.modelosPlanificacion.Actividad)

    modelTracker.register(models.modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada)
