from django.db.models import Q
from django.shortcuts import get_object_or_404

from core.base.models.modelosPlanificacionFormacion import PlanFormacionComplementaria
from core.base.models.modelosUsuario import Graduado
from core.base.permissions import CustomBasePermission, user_has_role


class IsGraduateTutorPermissions(CustomBasePermission):
    def _has_permission(self, request, view):
        user = request.user
        graduado = get_object_or_404(Graduado, pk=view.kwargs['graduadoID'])

        has_permission = graduado.tutores.filter(tutor_id=user.id, fechaRevocado=None).exists()
        view.kwargs['graduado'] = graduado
        return has_permission


class IsGraduateTutorOrJefeAreaPermissions(CustomBasePermission):
    def _has_permission(self, request, view):
        user = request.user
        graduado = get_object_or_404(Graduado, pk=view.kwargs['graduadoID'])

        is_tutor = graduado.tutores.filter(tutor_id=user.pk, fechaRevocado=None).exists()
        is_jefe = user.area_id == graduado.area_id and user_has_role(user, ['JEFE DE AREA'])

        view.kwargs['graduado'] = graduado
        has_permission = is_tutor or is_jefe
        return has_permission


class PlanPermission:
    def _get_plan(self, view_kwargs: dict) -> PlanFormacionComplementaria:
        plan = None
        if 'plan' in view_kwargs:
            return view_kwargs['plan']

        if 'planID' in view_kwargs:
            plan = get_object_or_404(PlanFormacionComplementaria, pk=view_kwargs['planID'])
        elif 'etapaID' in view_kwargs:
            plan = get_object_or_404(PlanFormacionComplementaria, etapas=view_kwargs['etapaID'])
        elif 'actividadID' in view_kwargs:
            plan = get_object_or_404(PlanFormacionComplementaria, etapas__actividades=view_kwargs['actividadID'])
        elif 'evaluacionID' in view_kwargs:
            plan = get_object_or_404(PlanFormacionComplementaria,
                                     Q(etapas__evaluacion=view_kwargs['evaluacionID']) |
                                     Q(evaluacion=view_kwargs['evaluacionID']))

        self.add_plan_to_view(view_kwargs, plan)
        return plan

    def add_plan_to_view(self, view_kwargs, plan):
        view_kwargs.setdefault('plan', plan)
        view_kwargs.setdefault('planID', plan.pk)


class IsPlanGraduatePermissions(CustomBasePermission, PlanPermission):

    def _has_permission(self, request, view):
        user = request.user
        plan = self._get_plan(view.kwargs)

        has_permission = user.pk == plan.graduado.pk
        return has_permission


class IsPlanTutorPermissions(CustomBasePermission, PlanPermission):
    def _has_permission(self, request, view):
        user = request.user
        plan = self._get_plan(view.kwargs)

        graduado = plan.graduado
        has_permission = graduado.tutores.filter(tutor_id=user.pk, graduado_id=graduado.pk, fechaRevocado=None).exists()
        return has_permission


class IsPlanJefeArea(CustomBasePermission, PlanPermission):
    def _has_permission(self, request, view):
        user = request.user
        plan = self._get_plan(view.kwargs)

        graduado = plan.graduado
        is_jefe = user.area_id == graduado.area_id and user_has_role(user, ['JEFE DE AREA'])

        has_permission = is_jefe
        return has_permission


class IsPlanTutorOrJefeAreaPermissions(CustomBasePermission, PlanPermission):
    def _has_permission(self, request, view):
        user = request.user
        plan = self._get_plan(view.kwargs)

        graduado = plan.graduado
        is_tutor = graduado.tutores.filter(tutor_id=user.pk, fechaRevocado=None).exists()
        is_jefe = user.area_id == graduado.area_id and user_has_role(user, ['JEFE DE AREA'])

        has_permission = is_tutor or is_jefe
        return has_permission
