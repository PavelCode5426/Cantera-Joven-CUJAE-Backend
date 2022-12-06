from django_filters.rest_framework import FilterSet

from core.base.models.modelosPlanificacionFormacion import PlanFormacionComplementaria


# TODO TERMINAR EL FILTERSET
class PlanFormacionComplementariaFilterSet(FilterSet):
    class Meta:
        model = PlanFormacionComplementaria
