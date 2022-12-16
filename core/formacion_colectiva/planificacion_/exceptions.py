from rest_framework import status
from rest_framework.exceptions import APIException


class FormacionHasNotStarted(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'La formacion no ha comenzado'
    default_code = 'formation_has_not_started'


class OnlyOnePlanColectivo(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ya existe un plan colectivo'
    default_code = 'only_one_plan_colectivo'


class CantUpdatePlanAfterApproved(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El plan no puede ser cambiado despues de aprobado'
    default_code = 'cant_update_plan_after_approved'


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
