from crum import get_current_user
from django_filters.rest_framework import FilterSet, filters

from core.base.models.modelosTutoria import SolicitudTutorExterno, TutoresAsignados


# TODO TERMINAR ESTO Y TRADUCIR AL INGLES
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
    no_revocation = filters.BooleanFilter(method='no_revocation_filter')

    def no_revocation_filter(self, queryset, name, value):
        queryset = queryset.filter(fechaRevocado__isnull=not value)
        return queryset

    class Meta:
        model = TutoresAsignados
        fields = ()
