from django_filters.rest_framework import FilterSet, filters

from core.base.models.modelosUsuario import Estudiante


class EstudianteFilterSet(FilterSet):
    has_aval = filters.BooleanFilter(field_name='aval', method='has_aval_filter')
    has_plan = filters.BooleanFilter(method='has_plan_filter')

    def has_aval_filter(self, queryset, name, value):
        aval = not bool(value)
        return queryset.filter(aval__isnull=aval)

    def has_plan_filter(self, queryset, name, value):
        plan = bool(value)
        if plan:
            queryset = queryset.filter(planformacioncantera__isnull=False)
        else:
            queryset = queryset.filter(planformacioncantera=None)
        return queryset

    class Meta:
        model = Estudiante
        fields = ()
