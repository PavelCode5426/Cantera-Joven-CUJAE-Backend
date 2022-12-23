from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    # Now add the HTTP status code to the response.
    if response is not None and hasattr(exc, 'default_code'):
        response.data['code'] = exc.default_code

    return response
