from rest_framework.generics import get_object_or_404

from core.base.models.modelosUsuario import Graduado
from core.base.permissions import CustomBasePermission, IsSameUserWhoRequestPermissions
from custom.authentication.models import DirectoryUser


class IsSameAreaPermissions(CustomBasePermission):

    def __has_permission(self, request, view):
        areaID = view.kwargs['areaID']
        has_permissions = request.user.area_id == areaID

        return has_permissions

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view) and self.__has_permission(request, view)
        is_superuser = request.user.is_superuser

        return has_permission or is_superuser


# COMPRUEBA QUE EL GRADUADO PASADO EN LA URL PERTENECE A LA MISMA AREA DE QUIEN CONSULTA
class GraduateOfSameAreaPermissions(CustomBasePermission):
    def __has_permission(self, request, view):
        graduado = view.kwargs.pop('graduadoID')
        graduado = get_object_or_404(Graduado, pk=graduado, area_id=request.user.area_id)
        view.kwargs['graduado'] = graduado
        has_permissions = graduado != None
        return has_permissions

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view) and self.__has_permission(request, view)
        is_superuser = request.user.is_superuser

        return has_permission or is_superuser


# COMPRUEBA QUE EL TUTOR PASADO EN LA URL PERTENECE A LA MISMA AREA DE QUIEN CONSULTA
class TutorOfSameAreaPermissions(CustomBasePermission):
    def __has_permission(self, request, view):
        tutor = view.kwargs.pop('tutorID')
        tutor = get_object_or_404(DirectoryUser, pk=tutor, area_id=request.user.area_id,
                                  graduado=None, posiblegraduado=None, estudiante=None)
        view.kwargs['tutor'] = tutor
        has_permissions = tutor != None
        return has_permissions

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view) and self.__has_permission(request, view)
        is_superuser = request.user.is_superuser

        return has_permission or is_superuser


class IsSameGraduateWhoRequestPermissions(IsSameUserWhoRequestPermissions):
    URL_KWARGS_KEY = 'graduateID'


class IsSameTutorWhoRequestPermissions(IsSameUserWhoRequestPermissions):
    URL_KWARGS_KEY = 'tutorID'
