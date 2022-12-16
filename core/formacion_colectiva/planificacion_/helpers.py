from core.base.models.modelosPlanificacion import Etapa, Plan
from core.base.models.modelosPlanificacionFamiliarizarcion import ActividadFamiliarizacion
from core.configuracion.helpers import config
from core.formacion_colectiva.planificacion_.exceptions import CantUpdatePlanAfterApproved


def can_manage_plan(plan: Plan) -> bool:
    if plan.is_approved:
        raise CantUpdatePlanAfterApproved
    return True


def can_manage_etapa(etapa: Etapa) -> bool:
    return can_manage_plan(etapa.plan)


def can_upload_file(actividad: ActividadFamiliarizacion) -> bool:
    if actividad.esGeneral or not config('planificar_formacion_colectiva'):
        can_manage_etapa(actividad.etapa)

    return True
