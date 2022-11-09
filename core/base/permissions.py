from rest_framework import permissions


def _user_has_role(user, roles: list):
    return user.groups.filter(name__in=roles).exists()


class CustomBasePermission(permissions.IsAuthenticated):

    def __has_permission(self, request, view):
        return True

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view) and self.__has_permission(request, view)
        is_superuser = request.user.is_superuser

        return has_permission or is_superuser


class IsRole(CustomBasePermission):
    role_name: list = []

    def __has_permission(self, request, view):
        has_permission = _user_has_role(request.user, self.role_name)
        return has_permission


class IsJefeArea(IsRole):
    role_name = ['Jefe de Area']


class IsDirectorRecursosHumanos(IsRole):
    role_name = ['Director de Recursos Humanos']


class IsTutor(IsRole):
    role_name = ['Tutor']


class IsEstudiante(IsRole):
    role_name = ['Estudiante']


class IsGraduado(IsRole):
    role_name = ['Graduado']


class IsSameUserWhoRequestPermissions(CustomBasePermission):
    URL_KWARGS_KEY = 'ID'

    def __has_permission(self, request, view):
        has_permissions = view.kargs[self.URL_KWARGS_KEY] == request.user.pk
        return has_permissions
