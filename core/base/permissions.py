from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from core.base.models.modelosSimple import Area


def _user_has_role(user, roles: list):
    have_role = user.groups.filter(name__in=roles).exists()
    return have_role


class CustomBasePermission(IsAuthenticated):

    def _has_permission(self, request, view):
        pass

    def has_permission(self, request, view):
        has_permission = super(IsAuthenticated, self).has_permission(request, view) \
                         and self._has_permission(request, view)
        is_superuser = request.user.is_superuser

        return has_permission or is_superuser


class IsRole(CustomBasePermission):
    role_name: list = []

    def _has_permission(self, request, view):
        has_permission = _user_has_role(request.user, self.role_name)
        return has_permission


class IsJefeArea(IsRole):
    role_name = ['JEFE DE AREA']


class IsDirectorRecursosHumanos(IsRole):
    role_name = ['DIRECTOR DE RECURSOS HUMANOS']


class IsTutor(IsRole):
    role_name = ['TUTOR']


class IsEstudiante(IsRole):
    role_name = ['ESTUDIANTE']


class IsGraduado(IsRole):
    role_name = ['GRADUADO']


class IsPosibleGraduado(IsRole):
    role_name = ['POSIBLE GRADUADO']


class IsVicerrector(IsRole):
    role_name = ['VICERRECTOR']


class IsSameUserWhoRequestPermissions(CustomBasePermission):
    URL_KWARGS_KEY = 'ID'

    def _has_permission(self, request, view):
        has_permissions = view.kargs[self.URL_KWARGS_KEY] == request.user.pk
        return has_permissions


class IsSameAreaPermissions(CustomBasePermission):

    def _has_permission(self, request, view):
        areaID = view.kwargs['areaID']
        has_permissions = request.user.area_id == areaID
        view.kwargs['area'] = get_object_or_404(Area, pk=areaID)

        return has_permissions
