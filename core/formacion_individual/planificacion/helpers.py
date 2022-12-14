from builtins import NotImplemented

from django.http import HttpResponse
from django.template.loader import get_template
from ics import Calendar, Event
from rest_framework.response import Response
from xhtml2pdf import pisa

from core.base.models.modelosPlanificacionFormacion import PlanFormacion, EtapaFormacion, \
    ActividadFormacion


class PlainExporter:

    def __init__(self, plan):
        self.plan = plan

    def export(self):
        raise NotImplemented


class PlainPDFExporter(PlainExporter):
    def export(self):

        plan_id = self.plan.pk
        plan = PlanFormacion.objects.select_related('evaluacion').get(pk=plan_id)
        etapa__actividad = []
        etapas = EtapaFormacion.objects.filter(plan_id=plan_id).all()
        for etapa in etapas:
            etapa__actividad.append((
                etapa,
                ActividadFormacion.objects.filter(etapa_id=etapa.pk, actividadPadre=None).all()
            ))

        context = {
            'plan': plan,
            'etapa__actividad': etapa__actividad
        }

        template = get_template('pdf/plan_formacion_complementaria_pdf.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="plan-formacion-individual.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return Response({'detail': 'Error al generar PDF'}, 500)
        return response


class PlainCalendarExporter(PlainExporter):
    def export(self):
        plan_id = self.plan.pk
        actividades = ActividadFormacion.objects.filter(etapa__plan_id=plan_id, actividadPadre=None).all()
        calendar = Calendar()

        for actividad in actividades:
            evento = Event()
            evento.name = actividad.nombre
            evento.description = actividad.descripcion
            evento.begin = actividad.fechaInicio
            evento.end = actividad.fechaFin
            calendar.events.add(evento)

        response = HttpResponse(calendar.serialize(), content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename="calendario.ics"'
        return response
