from django_filters.rest_framework import FilterSet

from core.base.models.modelosPlanificacionColectiva import ActividadColectiva


class ActividadColectivaFilterSet(FilterSet):
    class Meta:
        model = ActividadColectiva
        fields = ('area', 'esGeneral',)
