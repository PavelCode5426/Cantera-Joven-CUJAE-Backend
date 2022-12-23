from rest_framework.generics import get_object_or_404

from core.base.permissions import CustomBasePermission, IsSameUserWhoRequestPermissions
from custom.authentication.models import DirectoryUser


# class IsSameAreaPermissions(CustomBasePermission):
#
#     def __has_permission(self, request, view):
#         areaID = view.kwargs['areaID']
#         has_permissions = request.user.area_id == areaID
#
#         return has_permissions
#
#     def has_permission(self, request, view):
#         has_permission = super().has_permission(request, view) and self.__has_permission(request, view)
#         is_superuser = request.user.is_superuser
#
#         return has_permission or is_superuser


# COMPRUEBA QUE EL JOVEN PASADO EN LA URL PERTENECE A LA MISMA AREA DE QUIEN CONSULTA
class JovenOfSameAreaPermissions(CustomBasePermission):
    def _has_permission(self, request, view):
        joven = view.kwargs.get('jovenID')
        joven = get_object_or_404(DirectoryUser, pk=joven, area_id=request.user.area_id)
        view.kwargs.setdefault('joven', joven)
        has_permissions = joven is not None
        return has_permissions


# COMPRUEBA QUE EL TUTOR PASADO EN LA URL PERTENECE A LA MISMA AREA DE QUIEN CONSULTA
class TutorOfSameAreaPermissions(CustomBasePermission):
    def _has_permission(self, request, view):
        tutor = view.kwargs.get('tutorID')
        tutor = get_object_or_404(DirectoryUser, pk=tutor, area_id=request.user.area_id,
                                  graduado=None, posiblegraduado=None, estudiante=None)
        view.kwargs['tutor'] = tutor
        has_permissions = tutor is not None
        return has_permissions


class IsSameJovenWhoRequestPermissions(IsSameUserWhoRequestPermissions):
    URL_KWARGS_KEY = 'jovenID'

    def _has_permission(self, request, view):
        has_permissions = super()._has_permission(request, view)
        if has_permissions and not ('joven' in view.kwargs):
            pk = request.user.pk
            view.kwargs['joven'] = get_object_or_404(DirectoryUser, pk=pk)
        return has_permissions


class IsSameTutorWhoRequestPermissions(IsSameUserWhoRequestPermissions):
    URL_KWARGS_KEY = 'tutorID'

    def _has_permission(self, request, view):
        has_permissions = super()._has_permission(request, view)
        if has_permissions and not ('tutor' in view.kwargs):
            pk = request.user.pk
            view.kwargs['tutor'] = get_object_or_404(DirectoryUser, pk=pk)
        return has_permissions
