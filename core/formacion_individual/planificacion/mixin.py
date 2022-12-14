from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from core.base.models.modelosPlanificacionFormacion import EtapaFormacion, \
    ActividadFormacion, PlanFormacion
from core.formacion_individual.planificacion.exceptions import CantUpdatePlanAfterApproved, \
    CantUpdateEtapaAfterEvalutation, CantManageActividad
from core.formacion_individual.planificacion.helpers import PlainExporter


class PlanFormacionMixin(APIView):

    def have_plan_kwargs(self):
        if 'plan' not in self.kwargs and 'planID' not in self.kwargs:
            raise Exception('No cuenta con kwargs de plan en la vista')

    def plan_is_approved(self) -> bool:
        return self.get_plan().is_approved

    def get_planID(self):
        self.have_plan_kwargs()
        return self.kwargs.get('planID')

    def get_plan(self):
        self.have_plan_kwargs()
        return self.kwargs.get('plan', get_object_or_404(PlanFormacion, pk=self.get_planID()))

    def can_manage_plan(self) -> bool:
        plan = self.get_plan()
        if plan.is_approved:
            raise CantUpdatePlanAfterApproved
        return True


class EtapaFormacionMixin(PlanFormacionMixin):
    def get_etapaID(self):
        return self.kwargs.get('etapaID')

    def get_etapa(self, etapaID: int = None):
        if not etapaID:
            etapaID = self.get_etapaID()
        return get_object_or_404(EtapaFormacion, pk=etapaID)

    def etapa_is_evaluated(self, etapaID: int = None) -> bool:
        return self.get_etapa(etapaID).evaluacion_id is None

    def can_manage_etapa(self, etapaID: int = None) -> bool:
        self.can_manage_plan()
        if not self.etapa_is_evaluated(etapaID):
            raise CantUpdateEtapaAfterEvalutation
        return True


class EtapaFormacionMixinProxy(EtapaFormacionMixin):
    def get_etapa(self, etapaID: int = None):
        etapa = self.kwargs.get('etapa', super(EtapaFormacionMixinProxy, self).get_etapa(etapaID))
        self.kwargs.setdefault('etapa', etapa)
        return etapa


class ActividadFormacionMixin(EtapaFormacionMixinProxy):
    def get_actividadID(self):
        return self.kwargs.get('actividadID')

    def get_actividad(self, actividadID: int = None):
        if not actividadID:
            actividadID = self.get_actividadID()
        return get_object_or_404(ActividadFormacion, pk=actividadID)

    def can_manage_actividad(self, actividadID: int = None) -> bool:
        actividad = self.get_actividad(actividadID)
        return self.can_manage_etapa(actividad.etapa_id) or actividad.actividadPadre_id

    def can_change_actividad_status(self, actividadID: int = None) -> bool:
        actividad = self.get_actividad(actividadID)
        etapa = self.get_etapa(actividad.etapa_id)
        if etapa.evaluacion_id is not None or not self.plan_is_approved():
            raise CantManageActividad
        return True

    def can_manage_subactividades(self, actividadID: int = None):
        etapa_id = self.get_actividad(actividadID).etapa_id
        if self.plan_is_approved() and not self.etapa_is_evaluated(etapa_id):
            raise CantManageActividad
        return True


class ActividadFormacionMixinProxy(ActividadFormacionMixin):
    def get_actividad(self, actividadID: int = None):
        actividad = self.kwargs.get('actividad', super(ActividadFormacionMixinProxy, self).get_actividad(actividadID))
        self.kwargs.setdefault('actividad', actividad)
        return actividad


class PlanFormacionExportMixin(PlanFormacionMixin):
    plain_exporter_class: PlainExporter

    def get_exporter(self):
        plan = self.get_plan()
        return self.plain_exporter_class(plan)

    def get(self, request, *args, **kwargs):
        exporter = self.get_exporter()
        return exporter.export()
