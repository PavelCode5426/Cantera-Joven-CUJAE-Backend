from django_filters.rest_framework import FilterSet, filters

from core.base.models.modelosUsuario import PosibleGraduado


class PosibleGraduadoPreubicadoFilterSet(FilterSet):
    is_preubicado = filters.BooleanFilter(method='is_preubicado_filter')

    def is_preubicado_filter(self, queryset, name, value):
        esPreubicacion = not bool(value)
        return queryset.filter(ubicacionlaboraladelantada__esPreubicacion__isnull=esPreubicacion)

    class Meta:
        model = PosibleGraduado
        fields = ()
