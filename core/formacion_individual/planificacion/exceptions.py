from rest_framework import status
from rest_framework.exceptions import APIException


class FormacionHasNotStarted(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'La formacion individual no ha comenzado'
    default_code = 'formation_has_not_started'


class JovenHavePlan(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El joven ya tiene un plan de formacion individual'
    default_code = 'graduate_have_plan'


class JovenHaveNotPlan(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El joven no tiene plan de formacion individual'
    default_code = 'graduate_have_not_plan'


class CantUpdatePlanAfterApproved(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El plan no puede ser cambiado despues de aprobado'
    default_code = 'cant_update_plan_after_approved'


class CantUpdateEtapaAfterEvalutation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'La etapa no puede ser modificada despues de ser evaluada'
    default_code = 'cant_update_step_after_evaluation'


class CantManageActividad(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'La actividad no puede ser gestionada porque la etapa ha sido evaluada o el plan no ha sido aprobado'
    default_code = 'cant_manage_activity'


class CantEvaluateException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El recurso no puede ser evaluado'
    default_code = 'resource_cant_evaluate'


class EvaluacionAlreadyApproved(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'La evaluacion no puede ser cambiada despues de aprobada'
    default_code = 'cant_update_evaluation_after_approved'


class PlanAlreadyApproved(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El plan ya ha sido aprobado previamente'
    default_code = 'plain_already_approved'


class CantApproveResourceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El recurso no puede ser aprobado'
    default_code = 'resource_cant_approve'


class ResourceRequireEvaluationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El recurso requiere una evaluacion'
    default_code = 'require_evaluation'


class ResourceCantBeCommented(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El recurso no puede ser comentado'
    default_code = 'resource_cant_be_commented'
