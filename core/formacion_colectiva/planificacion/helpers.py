from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from requests import Response
from xhtml2pdf import pisa

from core.base.models.modelosPlanificacion import Etapa, Plan
from core.base.models.modelosPlanificacionColectiva import ActividadColectiva
from core.base.models.modelosSimple import Area
from core.configuracion.helpers import config
from core.formacion_colectiva.planificacion.exceptions import CantUpdatePlanAfterApproved


def can_manage_plan(plan: Plan) -> bool:
    if plan.is_approved:
        raise CantUpdatePlanAfterApproved
    return True


def can_manage_etapa(etapa: Etapa) -> bool:
    return can_manage_plan(etapa.plan)


def can_upload_file(actividad: ActividadColectiva) -> bool:
    if actividad.esGeneral or not config('planificar_formacion_colectiva'):
        can_manage_etapa(actividad.etapa)

    return True


class PlainExporter:

    def __init__(self, plan):
        self.plan = plan

    def export(self):
        raise NotImplemented


class PlainPDFExporter(PlainExporter):
    def export(self):
        plan = self.plan
        etapas = self.plan.etapas.order_by('fechaInicio')
        areas = Area.objects.all()

        etapa_area_actividades = []

        for area in areas:
            etapa_actividades = []
            for etapa in etapas:
                actividades = ActividadColectiva.objects \
                    .filter(Q(area=area, esGeneral=False) | Q(esGeneral=True), etapa=etapa) \
                    .order_by('-fechaInicio').all()

                etapa_actividades.append({
                    'etapa': etapa,
                    'actividades': actividades
                })

            etapa_area_actividades.append({
                'area': area,
                'etapas': etapa_actividades
            })

        context = {
            'plan': plan,
            'area_etapa_actividades': etapa_area_actividades
        }

        template = get_template('pdf/plan_colectivo_pdf.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="plan-formacion-colectivo.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return Response({'detail': 'Error al generar PDF'}, 500)
        return response
