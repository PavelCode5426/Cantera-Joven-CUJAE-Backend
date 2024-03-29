from rest_framework import status
from rest_framework.exceptions import APIException


class SelectedTutorNotFoundInArea(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Ha seleccionado un tutor que no pertenece a su area"
    default_code = 'tutor_not_found_in_area'


class SelectedTutorPreviuslyAssigned(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Ha seleccionado un tutor asignado anteriormente"
    default_code = 'tutor_previusly_assigned'


class SelectedGraduateHaveNotAvalException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Ha seleccionado un graduado que no tiene aval"
    default_code = 'graduate_need_aval'


class SelectedInvalidAreaException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No puede solicitar un tutor para el graduado de su propia area"
    default_code = 'selected_invalid_area'


class PreviouslyAnsweredRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Solicitud respondida anteriormente"
    default_code = 'previously_answered_request'


class GraduateRequireAvalException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Los graduados de nivel superior requieren aval antes de asignar tutor'
    default_code = 'graduate_require_aval'


class SelectedUserIsNotJovenException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Solamente se le puede asignar tutor a los jovenes'
    default_code = 'selected_user_is_not_joven'
