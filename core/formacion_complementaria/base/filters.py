from django_filters.rest_framework import FilterSet, filters

from core.base.models.modelosUsuario import Graduado


class GraduadoFilterSet(FilterSet):
    has_aval = filters.BooleanFilter(field_name='aval', method='has_aval_filter')
    has_tutor = filters.BooleanFilter(method='has_tutor_filter')
    has_plan = filters.BooleanFilter(method='has_plan_filter')

    def has_aval_filter(self, queryset, name, value):
        aval = not bool(value)
        return queryset.filter(aval__isnull=aval)

    def has_tutor_filter(self, queryset, name, value):
        tutor = bool(value)
        if tutor:
            queryset = queryset.filter(tutores__isnull=False, tutores__fechaRevocado=None)
            # MOSTRAR LOS QUE TENGAN ALGUN TUTOR SIN REVOCAR
        else:
            queryset = queryset.filter(tutores=None)  # TODO TERMINAR ESTO
            # MOSTRAR LOS QUE TENGAN TODOS LOS TUTORES REBOCADOS O NINGUN TUTOR
        return queryset

    def has_plan_filter(self, queryset, name, value):
        plan = bool(value)
        if plan:
            queryset = queryset.filter(planformacioncomplementaria__isnull=False)
        else:
            queryset = queryset.filter(planformacioncomplementaria=None)
        return queryset

    class Meta:
        model = Graduado
        fields = ('esExterno', 'esNivelSuperior')
