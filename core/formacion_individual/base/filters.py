from django_filters.rest_framework import FilterSet, filters

from custom.authentication.models import DirectoryUser


class JovenFilterSet(FilterSet):
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
            queryset = queryset.filter(
                planesformacion__isnull=False)  # TODO AJUSTAR ESTO PARA QUE SALGA CUANDO SE TERMINA EL PLAN
        else:
            queryset = queryset.filter(planesformacion=None)
        return queryset

    class Meta:
        model = DirectoryUser
        fields = []


class JovenAdvanceFilterSet(JovenFilterSet):
    is_student = filters.BooleanFilter(method='is_student_filter')
    is_graduate = filters.BooleanFilter(method='is_graduate_filter')

    def is_student_filter(self, query, name, value):
        student = bool(value)
        if student:
            query = query.filter(graduado=None)
        return query

    def is_graduate_filter(self, query, name, value):
        graduate = bool(value)
        if graduate:
            query = query.filter(graduado__isnull=False)
        return query
