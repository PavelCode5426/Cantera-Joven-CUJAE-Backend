from rest_framework.permissions import SAFE_METHODS

from core.base import permissions
from custom.authentication.models import DirectoryUser


class IsAvalOwnerOrJefeArea(permissions.CustomBasePermission):

    def _has_permission(self, request, view):
        has_permission = request.method in SAFE_METHODS

        if has_permission:
            user = request.user
            user_route_lookup = view.kwargs.get('usuario')
            has_permission = user.pk is user_route_lookup

            if not has_permission:
                has_permission = permissions._user_has_role(user, ['Jefe de Area', 'Tutor']) \
                                 and DirectoryUser.objects.filter(pk=user_route_lookup, area=user.area).exists()

        return has_permission
