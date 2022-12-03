from rest_framework.permissions import SAFE_METHODS

from core.base import permissions
from custom.authentication.models import DirectoryUser


class IsAvalOwner(permissions.CustomBasePermission):

    def _has_permission(self, request, view):
        user = request.user
        user_route_lookup = view.kwargs.get('usuarioID')
        has_permission = (request.method in SAFE_METHODS) and (user.pk is user_route_lookup)

        return has_permission


class IsAvalOwnerTutorOrJefeArea(permissions.CustomBasePermission):
    """PUEDEN OBTENER EL AVAL EL TUTOR Y EL JEFE DE AREA PERO SOLAMENTE LO PUEDE EDITAR EL JEFE DE AREA"""

    def _has_permission(self, request, view):
        user = request.user
        user_route_lookup = view.kwargs.get('usuarioID')

        if request.method in SAFE_METHODS:
            has_permission = permissions._user_has_role(user, ['JEFE DE AREA', 'TUTOR']) and \
                             DirectoryUser.objects.filter(pk=user_route_lookup, area=user.area).exists()
        else:
            has_permission = permissions._user_has_role(user, ['JEFE DE AREA']) and \
                             DirectoryUser.objects.filter(pk=user_route_lookup, area=user.area).exists()

        return has_permission
