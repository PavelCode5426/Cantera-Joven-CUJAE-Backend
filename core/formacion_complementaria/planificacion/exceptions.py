from rest_framework import status
from rest_framework.exceptions import APIException


class GraduateHavePlan(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El graduado ya tiene un plan de formacion complementaria'
    default_code = 'graduate_have_plan'


class GraduateHaveNotPlan(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El graduado no tiene plan de formacion complementaria'
    default_code = 'graduate_have_not_plan'


class CantUpdatePlanAfterApproved(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El plan no puede ser cambiado despues de aprobado'
    default_code = 'cant_update_plan_after_approved'


class CantEvaluateException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El recurso no puede ser evaluado'
    default_code = 'resource_cant_evaluate'


class CantApproveException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El recurso no puede ser aprobado'
    default_code = 'resource_cant_approve'


class ResourceNeedEvaluationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El recurso necesita una evaluacion'
    default_code = 'need_evaluation'
