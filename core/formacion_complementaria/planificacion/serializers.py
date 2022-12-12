import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers

from core.base.models.modelosPlanificacion import Comentario, Archivo
from core.base.models.modelosPlanificacionFormacion import PlanFormacionComplementaria, EtapaFormacion, \
    EvaluacionFormacion, EvaluacionFinal, ActividadFormacion
from core.base.validators import datetime_greater_now
from core.formacion_complementaria.base.serializers import GraduadoSerializer
from custom.authentication.serializer import DirectoryUserSerializer


class CommentsModelSerializer(serializers.ModelSerializer):
    texto = serializers.CharField()
    usuario = DirectoryUserSerializer(read_only=True, required=False)

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)

        if is_valid:
            view_kwargs: dict = self.context['view'].kwargs
            request = self.context['request']

            self._validated_data.setdefault('plan_id', view_kwargs.get('planID', None))
            self._validated_data.setdefault('actividad_id', view_kwargs.get('actividadID', None))
            self._validated_data.setdefault('usuario', request.user)

        return super().is_valid()

    class Meta:
        model = Comentario
        exclude = ('plan', 'actividad')


class EvaluacionFormacionModelSerializer(serializers.ModelSerializer):
    aprobadoPor = DirectoryUserSerializer(allow_null=True)

    class Meta:
        model = EvaluacionFormacion
        exclude = ()


class CrearEvaluacionFormacionModelSerializer(serializers.ModelSerializer):
    esSatisfactorio = serializers.BooleanField()

    class Meta:
        model = EvaluacionFormacion
        exclude = ('aprobadoPor',)


class CrearEvaluacionFinalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionFinal
        exclude = ()


class EtapaFormacionModelSerializer(serializers.ModelSerializer):
    numero = serializers.IntegerField(read_only=True)
    esProrroga = serializers.BooleanField(read_only=True)
    evaluacion = EvaluacionFormacionModelSerializer(allow_null=True, read_only=True)

    class Meta:
        model = EtapaFormacion
        exclude = ()


class UpdateEtapaFormacionSerializer(EtapaFormacionModelSerializer):
    objetivo = serializers.CharField(min_length=10, max_length=255)
    fechaInicio = serializers.DateTimeField(validators=[datetime_greater_now])
    fechaFin = serializers.DateTimeField(validators=[datetime_greater_now])

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)

        if is_valid:
            valid = self._validated_data

            if valid['fechaInicio'] > valid['fechaFin']:
                self._errors.setdefault('fechaInicio', ['Fecha mayor que la de fin'])
                self._errors.setdefault('fechaFin', ['Fecha menos que la de inicio'])

        return super().is_valid(raise_exception)

    class Meta:
        model = EtapaFormacion
        exclude = ('plan',)


class ArchivoModelSerializer(serializers.ModelSerializer):
    archivo = serializers.SerializerMethodField(method_name='file_full_url')

    def file_full_url(self, instance):
        request = self.context.get('request')
        file_url = instance.archivo.url
        return request.build_absolute_uri(file_url)

    class Meta:
        model = Archivo
        fields = ('fecha', 'archivo',)


class PlanFormacionComplementariaModelSerializer(serializers.ModelSerializer):
    graduado = GraduadoSerializer(read_only=True)
    # etapas = EtapaFormacionModelSerializer(many=True, read_only=True)
    aprobadoPor = DirectoryUserSerializer(allow_null=True, read_only=True)
    documento = serializers.SerializerMethodField(method_name='last_version', read_only=True, allow_null=True)

    def last_version(self, obj):
        archivo = obj.versiones.order_by('-fecha').first()
        if archivo:
            return ArchivoModelSerializer(instance=archivo, context=self.context).data
        return None

    class Meta:
        model = PlanFormacionComplementaria
        depth = 1
        exclude = ()


class UpdatePlanFormacionComplementariaSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=(
        ('DEV', 'En Desarrollo'),
        ('PEN', 'Pendiente de Revision')
    ))

    class Meta:
        model = PlanFormacionComplementaria
        fields = ('estado',)


class FirmarPlanFormacionSerializer(serializers.Serializer):
    sign = serializers.BooleanField()
    file = serializers.FileField(required=False)

    def is_valid(self, raise_exception=False):
        super(FirmarPlanFormacionSerializer, self).is_valid(raise_exception)

        validated_data = self._validated_data
        if validated_data.get('sign') and not validated_data.get('file', None):
            self._errors['file'] = [self.error_messages['required']]

        return super(FirmarPlanFormacionSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        plan: PlanFormacionComplementaria = validated_data.get('plan')
        if not validated_data.get('sign'):
            plan.estado = plan.Estados.RECHAZADO
        else:
            plan.estado = plan.Estados.APROBADO
            plan.aprobadoPor = validated_data.get('user')
            file = validated_data.get('file')

            extension = os.path.splitext(file.name)[1]
            plan.versiones.filter(versionado=False).delete()
            version = plan.versiones.filter(versionado=True).count() + 1
            file_system = FileSystemStorage()
            file = file_system.save(f'{settings.PFC_UPLOAD_ROOT}/plan_{plan.pk}/v_{version}{extension}', file)

            plan.versiones.create(plan_id=plan.pk, versionado=True, archivo=file)

        plan.save()
        return validated_data['sign']


class ActividadFormacionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadFormacion
        fields = '__all__'


class CreateUpdateActividadFormacionSerializer(serializers.ModelSerializer):
    fechaInicio = serializers.DateTimeField(validators=[datetime_greater_now])
    fechaFin = serializers.DateTimeField(validators=[datetime_greater_now])

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)

        if is_valid:
            valid = self._validated_data

            if valid['fechaInicio'] > valid['fechaFin']:
                self._errors.setdefault('fechaInicio', ['Fecha mayor que la de fin'])
                self._errors.setdefault('fechaFin', ['Fecha menos que la de inicio'])

        return super().is_valid(raise_exception)

    def create(self, validated_data: dict):
        if not validated_data.get('etapa', None):
            raise Exception('Falta la etapa en los datos validos')

        actividad = ActividadFormacion.objects.create(**validated_data)
        return actividad

    class Meta:
        model = ActividadFormacion
        fields = ('nombre', 'descripcion', 'observacion', 'participantes', 'responsable', 'fechaInicio', 'fechaFin',)


class CambiarEstadoActividadFormacion(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=(
        ('REV', 'Revisada'),
        ('PAR', 'Parcialmente Cumplida'),
        ('CUM', 'Cumplida'),
        ('INCUM', 'Incumplida'),
    ))

    class Meta:
        model = ActividadFormacion
        fields = ('estado',)
