from . import modelosPlanificacion
from . import modelosPlanificacionCantera
from . import modelosPlanificacionFamiliarizarcion
from . import modelosPlanificacionFormacionComplementaria
from . import modelosSimple
from . import modelosTutoria
from . import modelosUsuario
from . import modelosAbstractos



adminModels=[
    #Planificacion
    modelosPlanificacion.Evaluacion,
    modelosPlanificacion.Actividad,
    modelosPlanificacion.Plan,
    modelosPlanificacion.Etapa,
    modelosPlanificacion.Comentario,
    modelosPlanificacion.Entregable,
    modelosPlanificacion.FirmadoPor,
    modelosPlanificacion,
]
adminModels+=[
    #Simples
    modelosSimple.Area,
    modelosSimple.Dimension,
    modelosSimple.LugarProcedencia,
    modelosSimple.Registro,
    modelosSimple.Alertas,
    modelosSimple.Configuracion,
    modelosSimple.PropuestaMovimiento,
]
adminModels+=[
    #Tutoria
    modelosTutoria.GraduadoTutor,
    modelosTutoria.SolicitudTutorExterno,
]
adminModels+=[
    #Usuarios
    modelosUsuario.PosibleGraduado,
    modelosUsuario.Estudiante,
    modelosUsuario.Aval,
    modelosUsuario.Graduado,
]
adminModels+=[
    #Familiarizacion
    modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada,
]