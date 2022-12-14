from django.db.models import Q
from django.shortcuts import get_object_or_404
from lxml.html.builder import Q

from core.base.models.modelosPlanificacionFormacion import PlanFormacion
from core.base.permissions import CustomBasePermission, user_has_role
from custom.authentication.models import DirectoryUser


class IsJovenTutorPermissions(CustomBasePermission):
    def _has_permission(self, request, view):
        user = request.user
        joven = get_object_or_404(DirectoryUser, pk=view.kwargs['jovenID'])

        has_permission = joven.tutores.filter(tutor_id=user.id, fechaRevocado=None).exists()
        view.kwargs.setdefault('joven', joven)
        return has_permission


class IsGraduateTutorOrJefeAreaPermissions(CustomBasePermission):
    def _has_permission(self, request, view):
        user = request.user
        joven = get_object_or_404(DirectoryUser, pk=view.kwargs['jovenID'])

        is_tutor = joven.tutores.filter(tutor_id=user.pk, fechaRevocado=None).exists()
        is_jefe = user.area_id == joven.area_id and user_has_role(user, ['JEFE DE AREA'])

        view.kwargs.setdefault('joven', joven)
        has_permission = is_tutor or is_jefe
        return has_permission


class PlanPermission:
    def _get_plan(self, view_kwargs: dict) -> PlanFormacion:
        plan = None
        if 'plan' in view_kwargs:
            return view_kwargs['plan']

        if 'planID' in view_kwargs:
            plan = get_object_or_404(PlanFormacion, pk=view_kwargs['planID'])
        elif 'etapaID' in view_kwargs:
            plan = get_object_or_404(PlanFormacion, etapas=view_kwargs['etapaID'])
        elif 'actividadID' in view_kwargs:
            plan = get_object_or_404(PlanFormacion, etapas__actividades=view_kwargs['actividadID'])
        elif 'archivoID' in view_kwargs:
            plan = get_object_or_404(PlanFormacion, etapas__actividades__documentos=view_kwargs['archivoID'])
        elif 'evaluacionID' in view_kwargs:
            plan = get_object_or_404(PlanFormacion, Q(etapas__evaluacion=view_kwargs['evaluacionID']) | Q(
                evaluacion=view_kwargs['evaluacionID']))

        self.add_plan_to_view(view_kwargs, plan)
        return plan

    def add_plan_to_view(self, view_kwargs, plan):
        view_kwargs.setdefault('plan', plan)
        view_kwargs.setdefault('planID', plan.pk)


class IsPlanJovenPermissions(CustomBasePermission, PlanPermission):

    def _has_permission(self, request, view):
        user = request.user
        plan = self._get_plan(view.kwargs)

        has_permission = user.pk == plan.joven_id
        return has_permission


class IsPlanTutorPermissions(CustomBasePermission, PlanPermission):
    def _has_permission(self, request, view):
        user = request.user
        plan = self._get_plan(view.kwargs)

        joven = plan.joven
        has_permission = joven.tutores.filter(tutor_id=user.pk, joven_id=joven.pk, fechaRevocado=None).exists()
        return has_permission


class IsPlanJefeArea(CustomBasePermission, PlanPermission):
    def _has_permission(self, request, view):
        user = request.user
        plan = self._get_plan(view.kwargs)

        joven = plan.joven
        is_jefe = user.area_id == joven.area_id and user_has_role(user, ['JEFE DE AREA'])

        has_permission = is_jefe
        return has_permission


class IsPlanTutorOrJefeAreaPermissions(CustomBasePermission, PlanPermission):
    def _has_permission(self, request, view):
        user = request.user
        plan = self._get_plan(view.kwargs)

        joven = plan.joven
        is_tutor = joven.tutores.filter(tutor_id=user.pk, fechaRevocado=None).exists()
        is_jefe = user.area_id == joven.area_id and user_has_role(user, ['JEFE DE AREA'])

        has_permission = is_tutor or is_jefe
        return has_permission
