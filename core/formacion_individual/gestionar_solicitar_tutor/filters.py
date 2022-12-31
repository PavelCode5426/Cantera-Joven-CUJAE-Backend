from crum import get_current_user
from django_filters.rest_framework import FilterSet, filters

from core.base.models.modelosPlanificacionIndividual import SolicitudTutorExterno, TutoresAsignados


class SolicitudTutorFilterSet(FilterSet):
    is_pendiente = filters.BooleanFilter(method='is_pendiente_filter')
    is_enviada = filters.BooleanFilter(method='is_enviada_filter')

    def is_pendiente_filter(self, queryset, name, value):
        queryset = queryset.filter(fechaRespuesta__isnull=value)
        return queryset

    def is_enviada_filter(self, queryset, name, value):
        user = get_current_user()
        if value:
            queryset = queryset.exclude(area_id=user.area_id)
        else:
            queryset = queryset.filter(area_id=user.area_id)
        return queryset

    class Meta:
        model = SolicitudTutorExterno
        fields = ('joven', 'area')

        """
        HACER EL FILTRADO Y EL MOSTRADO DE LAS SOLICITUDES
        ARREGLAR Y REVISAR TODO LO QUE SE HA PROGRAMADO
        PENSAR EN UNA NUEVA SOLUCION PARA LOS PLANES
    
        """


class TutoriaFilterSet(FilterSet):
    revocado = filters.BooleanFilter(method='revocado_filter')

    def revocado_filter(self, queryset, name, value):
        queryset = queryset.filter(fechaRevocado__isnull=not bool(value))
        return queryset

    class Meta:
        model = TutoresAsignados
        fields = ()


class TutoriaPorTutorFilterSet(TutoriaFilterSet):
    has_aval = filters.BooleanFilter(field_name='aval', method='has_aval_filter')
    has_plan = filters.BooleanFilter(method='has_plan_filter')

    def has_aval_filter(self, queryset, name, value):
        aval = not bool(value)
        return queryset.filter(joven__aval__isnull=aval)

    def has_plan_filter(self, queryset, name, value):
        plan = bool(value)
        if plan:
            queryset = queryset.filter(
                joven__planesformacion__isnull=False)  # TODO AJUSTAR ESTO PARA QUE SALGA CUANDO SE TERMINA EL PLAN
        else:
            queryset = queryset.filter(joven__planesformacion=None)
        return queryset
