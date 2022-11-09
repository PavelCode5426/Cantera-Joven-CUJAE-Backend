from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyHaveAvalException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'El usuario ya cuenta con un aval'
    default_code = 'error'
