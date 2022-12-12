from django_filters.rest_framework import FilterSet

from core.base.models.modelosPlanificacionFormacion import PlanFormacionComplementaria


# from django_filters.rest_framework import filters


# TODO TERMINAR EL FILTERSET
class PlanFormacionComplementariaFilterSet(FilterSet):
    # evaluado = filters.BooleanFilter(method=)

    class Meta:
        model = PlanFormacionComplementaria
