from django_filters.rest_framework import FilterSet, filters

from core.base.models.modelosPlanificacion import Evaluacion
from core.base.models.modelosPlanificacionIndividual import PlanFormacion


class PlanFormacionFilterSet(FilterSet):
    class Meta:
        model = PlanFormacion
        fields = ['estado']


class EvaluacionFilterSet(FilterSet):
    pendiente = filters.BooleanFilter(method='pendiente_filter')

    # TODO PROPONGO PONER FILTRADO POR PROPUESTA DE MOVIMIENTO, CERRAR PLAN O REPLANIFICAR

    def pendiente_filter(self, queryset, name, value):
        queryset = queryset.filter(aprobadoPor__isnull=value)
        return queryset

    class Meta:
        model = Evaluacion
        fields = ['esSatisfactorio']
