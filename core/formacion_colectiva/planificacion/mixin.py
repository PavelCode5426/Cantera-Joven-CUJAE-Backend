# TODO OPTIMIZAR LOS GET DE FORMA TAL QUE GUARDE LOS DATOS EN EL KWARG ANTES DE RETORNARLO
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from core.base.models.modelosPlanificacion import Plan, Etapa
from core.base.models.modelosPlanificacionColectiva import ActividadColectiva
# from core.formacion_individual.planificacion.helpers import PlainExporter
from core.formacion_colectiva.planificacion.helpers import PlainExporter


class PlanColectivoMixin(APIView):
    plan_url_kwarg = 'planID'

    def have_plan_kwargs(self):
        if 'plan' not in self.kwargs and self.plan_url_kwarg not in self.kwargs:
            raise Exception('No cuenta con kwargs de plan en la vista')

    def plan_is_approved(self) -> bool:
        return self.get_plan().is_approved

    def get_planID(self):
        self.have_plan_kwargs()
        return self.kwargs.get(self.plan_url_kwarg)

    def get_plan(self):
        self.have_plan_kwargs()
        plan = self.kwargs.get('plan', get_object_or_404(Plan, pk=self.get_planID(), planformacion=None))
        self.kwargs.setdefault('plan', plan)
        return plan


class EtapaColectivaMixin(APIView):
    etapa_url_kwarg = 'etapaID'

    def get_etapaID(self):
        return self.kwargs.get(self.etapa_url_kwarg)

    def get_etapa(self, etapaID: int = None):
        if not etapaID:
            etapaID = self.get_etapaID()
        etapa = self.kwargs.get('etapa', get_object_or_404(Etapa, pk=etapaID, plan__planformacion=None))
        self.kwargs.setdefault('etapa', etapa)
        return etapa


class ActividadColectivaMixin(APIView):
    actividad_url_kwarg = 'actividadID'

    def get_actividadID(self):
        return self.kwargs.get(self.actividad_url_kwarg)

    def get_actividad(self, actividadID: int = None):
        if not actividadID:
            actividadID = self.get_actividadID()
        actividad = self.kwargs.get('actividad', get_object_or_404(ActividadColectiva, pk=actividadID))
        self.kwargs.setdefault('actividad', actividad)
        return actividad


class PlanColectivoExportMixin(PlanColectivoMixin):
    plain_exporter_class: PlainExporter

    def get_exporter(self):
        plan = self.get_plan()
        return self.plain_exporter_class(plan)

    def get(self, request, *args, **kwargs):
        exporter = self.get_exporter()
        return exporter.export()
