from crum import get_current_user
from django.contrib.auth.models import Group
from django.db.models import Count, F
from django.utils.timezone import now
from rest_framework import serializers

from core.base.models.modelosPlanificacionIndividual import TutoresAsignados, SolicitudTutorExterno
from core.formacion_individual.gestionar_solicitar_tutor.helpers import get_all_tutors
from custom.authentication.models import DirectoryUser
from custom.authentication.serializer import DirectoryUserSerializer
from .exceptions import SelectedTutorNotFoundInArea, \
    SelectedTutorPreviuslyAssigned
from ..base.serializers import JovenSerializer
from ...base.models.modelosSimple import Area
from ...formacion_colectiva.gestionar_area.serializers import AreaSerializer


class TutoresDelGraduadoSerializer(serializers.ModelSerializer):
    tutor = DirectoryUserSerializer()

    class Meta:
        model = TutoresAsignados
        exclude = ['joven']
        deph = 1


class TutoradosDelTutorSerializer(serializers.ModelSerializer):
    joven = JovenSerializer()

    class Meta:
        model = TutoresAsignados
        exclude = ['tutor']
        deph = 1


class SolicitudSerializer(serializers.Serializer):
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    motivo_solicitud = serializers.CharField()

    def validate_area(self, value):
        user = get_current_user()
        if hasattr(user, 'area') and value == user.area:
            raise serializers.ValidationError('No puede solicitar un tutor de su misma area')
        return value


class AsignarSolicitarTutorSerializer(serializers.Serializer):
    tutores = serializers.PrimaryKeyRelatedField(many=True, queryset=get_all_tutors())
    solicitudes = SolicitudSerializer(many=True, required=False)

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)

        if is_valid:

            joven = self.initial_data['joven']
            area = joven.area
            self._validated_data['joven'] = self.initial_data['joven']

            # COMPROBAR QUE TODOS LOS TUTORES SON DE LA MISMA AREA
            tutores_externos_no_revocados = DirectoryUser.objects \
                .filter(tutorados__joven=joven, tutorados__fechaRevocado__isnull=True) \
                .exclude(area=area).all()
            for tutor in self._validated_data['tutores']:
                if tutor.area != area and not (tutor in tutores_externos_no_revocados):
                    raise SelectedTutorNotFoundInArea

        return not bool(self._errors)

    def create(self, validated_data):
        result = {}
        joven = validated_data['joven']

        if 'tutores' in validated_data:
            tutores = validated_data['tutores']
            joven.tutores.exclude(tutor__in=tutores, fechaRevocado__isnull=True).update(fechaRevocado=now())

            tutores_sin_tutorados = DirectoryUser.objects \
                .filter(tutorados__fechaRevocado__isnull=False, groups__name__in=['TUTOR']) \
                .annotate(revocados=Count('tutorados__fechaRevocado'), asignados=Count('tutorados')) \
                .filter(revocados=F('asignados')).all()

            role = Group.objects.get_or_create(name='TUTOR', defaults={'name': 'TUTOR'})[0]
            for tutor in tutores_sin_tutorados:
                role.user_set.remove(tutor)

            # TODO LAURA QUITAR ROLE DE TUTOR A LOS TUTORES SIN TUTORADOS
            # SELECT * FROM TUTORASIGNADO WHERE ALL(TUTOR.REVOCADO = TRUE) #LA CONSULTA PARA OBTENER LOS TUTORES
            # SINO PONLO EN UN TRIGGER DE POSTGRESQL
            # TODO ESTO LO HICE, REVISA QUE FUNCIONE BIEN

            for tutor in tutores:
                data = dict(tutor=tutor)
                joven.tutores.get_or_create(defaults=data, tutor=tutor, fechaRevocado=None)
                tutor.groups.add(role)

            result['tutores'] = tutores

        if 'solicitudes' in validated_data:
            solicitudes = list()
            for solicitud in validated_data['solicitudes']:
                data = dict(**solicitud, joven=joven, fechaCreado=now())
                solicitudes.append(
                    SolicitudTutorExterno.objects.update_or_create(
                        defaults=data,
                        area=solicitud['area'],
                        joven=joven,
                        respuesta=None
                    ))
            result['solicitudes'] = solicitudes

        return result


class SolicitudTutorExternoSerializer(serializers.ModelSerializer):
    # area = serializers.SerializerMethodField(method_name='area_name')
    joven = JovenSerializer()
    area = AreaSerializer()

    class Meta:
        model = SolicitudTutorExterno
        fields = '__all__'
        depth = 1


class SolicitudTutorExternoWithoutMotivoSerializer(SolicitudTutorExternoSerializer):
    area = AreaSerializer()

    class Meta:
        model = SolicitudTutorExterno
        exclude = ('motivo_respuesta', 'motivo_solicitud')
        depth = 1


class ResponderSolicitudSerializer(serializers.Serializer):
    tutores = serializers.PrimaryKeyRelatedField(many=True, queryset=get_all_tutors())
    motivo_respuesta = serializers.CharField()

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)

        # COMPROBAR QUE TODOS LOS TUTORES SON DE LA MISMA AREA
        area = self.initial_data['area']
        solicitud = self.initial_data['solicitud']
        joven = solicitud.joven

        tutores_asignados_del_area = DirectoryUser.objects.filter(tutorados__joven=joven,
                                                                  tutorados__fechaRevocado__isnull=True,
                                                                  area=area).all()
        for tutor in self._validated_data['tutores']:
            if tutor.area != area:
                raise SelectedTutorNotFoundInArea
            elif tutor in tutores_asignados_del_area:
                raise SelectedTutorPreviuslyAssigned

        self._validated_data['area'] = area
        self._validated_data['solicitud'] = solicitud
        self._validated_data['joven'] = joven

        return super(ResponderSolicitudSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        solicitud = validated_data['solicitud']
        joven = validated_data['joven']
        tutores = validated_data['tutores']
        motivo_respuesta = validated_data['motivo_respuesta']

        solicitud.motivo_respuesta = motivo_respuesta
        solicitud.fechaRespuesta = now()
        solicitud.respuesta = len(tutores)
        solicitud.save()

        asignar_tutores = list()
        for tutor in tutores:
            asignar_tutores.append(TutoresAsignados(tutor=tutor, joven=joven))
        TutoresAsignados.objects.bulk_create(asignar_tutores)

        return solicitud
