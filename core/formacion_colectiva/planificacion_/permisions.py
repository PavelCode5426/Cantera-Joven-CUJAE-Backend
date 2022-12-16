from rest_framework.generics import get_object_or_404

from core.base.models.modelosUsuario import PosibleGraduado
from core.base.permissions import IsSameUserWhoRequestPermissions, IsSameAreaPermissions


class IsSamePosibleGraduado(IsSameUserWhoRequestPermissions):
    URL_KWARGS_KEY = 'jovenID'


class IsSameAreaJefeArea(IsSameAreaPermissions):
    def _has_permission(self, request, view):
        kwargs = view.kwargs
        joven = get_object_or_404(PosibleGraduado, pk=kwargs.get('jovenID'))
        kwargs.set('joven', joven)
        return joven.area_id == request.user.area_id
