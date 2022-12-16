from django_filters.rest_framework import FilterSet

from core.base.models.modelosPlanificacionFamiliarizarcion import ActividadFamiliarizacion


class ActividadColectivaFilterSet(FilterSet):
    class Meta:
        model = ActividadFamiliarizacion
        fields = ('area', 'esGeneral',)
