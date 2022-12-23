from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS

from core.base.models.modelosPlanificacionIndividual import SolicitudTutorExterno
from core.base.permissions import CustomBasePermission


class SendOrReciveSolicitudTutorExternoPermissions(CustomBasePermission):
    """
    REVISA QUE QUIEN REVISA LA SOLICITUD DE TUTOR TENGA PERMISOS PARA HACERLO,
    COMPROBANDO QUE SEA QUIEN LA ENVIO O PARA QUIEN FUE ENVIADA.
    """

    def _has_permission(self, request, view):
        solicitud = view.kwargs['solicitudID']
        area = request.user.area

        try:
            solicitud = get_object_or_404(SolicitudTutorExterno, Q(joven__area=area) | Q(area=area), pk=solicitud)
        except SolicitudTutorExterno.DoesNotExist:
            solicitud = None

        view.kwargs.setdefault('solicitud', solicitud)
        has_permissions = solicitud != None

        if request.method not in SAFE_METHODS and has_permissions:
            # SOLAMENTE PUEDE ACCEDER A CAMBIAR LOS DATOS QUIEN RECIBA LA SOLICITUD
            has_permissions = solicitud.area == area

        return has_permissions
