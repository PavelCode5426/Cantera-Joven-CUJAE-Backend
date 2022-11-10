from crum import get_current_user
from django_filters.rest_framework import FilterSet, filters
from core.base.models.modelosUsuario import PosibleGraduado
from core.base.models.modelosPlanificacionFamiliarizarcion import UbicacionLaboralAdelantada

class PosibleGraduadoPreubicadoFilterSet(FilterSet):
    is_preubicado = filters.BooleanFilter(method='is_preubicado_filter')

    def is_preubicado_filter(self, queryset, name, value):
        esPreubicacion = not bool(value)
        return queryset.filter(esPreubicacion__isnull=esPreubicacion)

    class Meta:
        model = UbicacionLaboralAdelantada
        fields = ()
