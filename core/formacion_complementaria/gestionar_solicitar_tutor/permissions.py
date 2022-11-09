from django.db.models import Q
from rest_framework.permissions import SAFE_METHODS

from core.base.models.modelosTutoria import SolicitudTutorExterno
from core.base.permissions import CustomBasePermission


class SendOrReciveSolicitudTutorExternoPermissions(CustomBasePermission):
    """
    REVISA QUE QUIEN REVISA LA SOLICITUD DE TUTOR TENGA PERMISOS PARA HACERLO,
    COMPROBANDO QUE SEA QUIEN LA ENVIO O PARA QUIEN FUE ENVIADA.
    """

    def __has_permission(self, request, view):
        solicitud = view.kwargs['solicitudID']
        area = request.user.area

        try:
            solicitud = SolicitudTutorExterno.objects.get(Q(graduado__area=area) | Q(area=area), pk=solicitud)
        except SolicitudTutorExterno.DoesNotExist:
            solicitud = None

        view.kwargs['solicitud'] = solicitud
        has_permissions = solicitud != None

        if request.method not in SAFE_METHODS and has_permissions:
            # SOLAMENTE PUEDE ACCEDER A CAMBIAR LOS DATOS QUIEN RECIBA LA SOLICITUD
            has_permissions = solicitud.area == area

        return has_permissions

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view) and self.__has_permission(request, view)
        is_superuser = request.user.is_superuser

        return has_permission or is_superuser
