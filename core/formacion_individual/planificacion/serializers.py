import os

from crum import get_current_request
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.base.models.modelosPlanificacion import Comentario, Archivo, Evaluacion
from core.base.models.modelosPlanificacionIndividual import EtapaFormacion, \
    EvaluacionFormacion, EvaluacionFinal, ActividadFormacion, PlanFormacion
from core.base.models.modelosSimple import PropuestaMovimiento, Dimension
from core.base.validators import datetime_greater_now
from core.formacion_individual.base.serializers import JovenSerializer
from custom.authentication.models import DirectoryUser
from custom.authentication.serializer import DirectoryUserSerializer


class PropuestaMovimientoModelSerializer(ModelSerializer):
    class Meta:
        model = PropuestaMovimiento
        fields = '__all__'


class DimensionModelSerializer(ModelSerializer):
    class Meta:
        model = Dimension
        fields = '__all__'


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
    joven = serializers.SerializerMethodField()
    etapa = serializers.SerializerMethodField()

    def get_joven(self, object):
        joven = DirectoryUser.objects.filter(planesformacion__etapas__etapaformacion__evaluacion_id=object.pk).first()
        return DirectoryUserSerializer(joven).data

    def get_etapa(self, object):
        etapa = EtapaFormacion.objects.filter(evaluacion_id=object.pk).first()
        return EtapaFormacionWithOutEvaluacionModelSerializer(etapa).data

    class Meta:
        model = EvaluacionFormacion
        exclude = ()


class EvaluacionFinalModelSerializer(serializers.ModelSerializer):
    aprobadoPor = DirectoryUserSerializer(allow_null=True)
    propuestaMovimiento = PropuestaMovimientoModelSerializer(allow_null=True)
    joven = serializers.SerializerMethodField()

    plan = serializers.SerializerMethodField()

    def get_joven(self, object):
        joven = DirectoryUser.objects.filter(
            Q(planesformacion__evaluacion_id=object.pk) | Q(planesformacion__evaluacion_prorroga_id=object.pk)).first()
        return DirectoryUserSerializer(joven).data

    def get_plan(self, object):
        plan = PlanFormacion.objects.filter(Q(evaluacion_id=object.pk) | Q(evaluacion_prorroga_id=object.pk)).first()
        return AuxPlanFormacionModelSerializer(plan).data

    class Meta:
        model = EvaluacionFinal
        exclude = ()


class EvaluacionModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance: Evaluacion):
        if instance.is_evaluacion_formacion:
            representation = EvaluacionFormacionModelSerializer(instance=instance.evaluacionformacion).data
        elif instance.is_evaluacion_final:
            representation = EvaluacionFinalModelSerializer(instance=instance.evaluacionfinal).data
        else:
            representation = super(EvaluacionModelSerializer, self).to_representation(instance)
        return representation

    class Meta:
        model = Evaluacion
        exclude = ()


class CrearEvaluacionFormacionModelSerializer(serializers.ModelSerializer):
    esSatisfactorio = serializers.BooleanField()

    class Meta:
        model = EvaluacionFormacion
        exclude = ('aprobadoPor',)


class CrearEvaluacionFinalModelSerializer(serializers.ModelSerializer):

    def is_valid(self, raise_exception=False):
        super(CrearEvaluacionFinalModelSerializer, self).is_valid(raise_exception)

        validated_data = self._validated_data
        if self.context.get('esProrroga', False):
            propuestaMovimiento = validated_data.get('propuestaMovimiento')
        return super(CrearEvaluacionFinalModelSerializer, self).is_valid(raise_exception)

    class Meta:
        model = EvaluacionFinal
        exclude = ()


class EtapaFormacionWithOutEvaluacionModelSerializer(serializers.ModelSerializer):
    numero = serializers.IntegerField(read_only=True)
    esProrroga = serializers.BooleanField(read_only=True)
    dimension = DimensionModelSerializer(allow_null=True, read_only=True)

    class Meta:
        model = EtapaFormacion
        exclude = ('evaluacion',)


class EtapaFormacionModelSerializer(serializers.ModelSerializer):
    numero = serializers.IntegerField(read_only=True)
    esProrroga = serializers.BooleanField(read_only=True)
    dimension = DimensionModelSerializer(allow_null=True, read_only=True)
    evaluacion = EvaluacionFormacionModelSerializer(allow_null=True, read_only=True)

    class Meta:
        model = EtapaFormacion
        exclude = ()


class UpdateEtapaFormacionSerializer(EtapaFormacionModelSerializer):
    objetivo = serializers.CharField(min_length=10, max_length=255)
    dimension = None
    fechaInicio = serializers.DateTimeField(validators=[datetime_greater_now])
    fechaFin = serializers.DateTimeField(validators=[datetime_greater_now])

    def is_valid(self, raise_exception=False):
        is_valid = super(UpdateEtapaFormacionSerializer, self).is_valid(raise_exception)

        if is_valid:
            valid = self._validated_data

            if valid['fechaInicio'] > valid['fechaFin']:
                self._errors.setdefault('fechaInicio', ['Fecha mayor que la de fin'])
                self._errors.setdefault('fechaFin', ['Fecha menos que la de inicio'])

        return super(UpdateEtapaFormacionSerializer, self).is_valid(raise_exception)

    class Meta:
        model = EtapaFormacion
        exclude = ('plan',)


class ArchivoModelSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField(method_name='file_full_name')
    size = serializers.SerializerMethodField(method_name='file_size')
    archivo = serializers.SerializerMethodField(method_name='file_full_url')

    def file_full_url(self, instance):
        request = self.context.get('request', get_current_request())
        file_url = instance.archivo.url
        return request.build_absolute_uri(file_url)

    def file_full_name(self, instance):
        name = instance.archivo.name
        last_index = name.rindex('/') + 1
        return name[last_index:]

    def file_size(self, instance):
        return instance.archivo.size

    class Meta:
        model = Archivo
        fields = ('id', 'nombre', 'size', 'fecha', 'archivo',)


class PlanFormacionWithoutJoveModelSerializer(serializers.ModelSerializer):
    aprobadoPor = DirectoryUserSerializer(allow_null=True, read_only=True)
    documento = serializers.SerializerMethodField(method_name='last_version', read_only=True, allow_null=True)

    def last_version(self, obj):
        archivo = obj.versiones.order_by('-fecha').first()
        if archivo:
            return ArchivoModelSerializer(instance=archivo, context=self.context).data
        return None

    class Meta:
        model = PlanFormacion
        depth = 1
        exclude = ('joven',)


class PlanFormacionModelSerializer(PlanFormacionWithoutJoveModelSerializer):
    joven = JovenSerializer(read_only=True)
    evaluacion = EvaluacionFinalModelSerializer(read_only=True, allow_null=True)
    evaluacion_prorroga = EvaluacionFinalModelSerializer(read_only=True, allow_null=True)

    class Meta:
        model = PlanFormacion
        depth = 1
        exclude = ()


class UpdatePlanFormacionSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=(
        'En Desarrollo',
        'Pendiente de Revision'
    ))

    class Meta:
        model = PlanFormacion
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
        plan: PlanFormacion = validated_data.get('plan')
        if not validated_data.get('sign'):
            plan.estado = plan.Estados.RECHAZADO
        else:
            plan.estado = plan.Estados.APROBADO
            plan.aprobadoPor = validated_data.get('user')
            file = validated_data.get('file')

            extension = os.path.splitext(file.name)[1]
            version = plan.versiones.count() + 1
            file_system = FileSystemStorage()
            file = file_system.save(f'{settings.PFI_UPLOAD_ROOT}/plan_{plan.pk}/v_{version}{extension}', file)

            plan.versiones.create(plan_id=plan.pk, archivo=file)

        plan.save()
        return validated_data['sign']


# class ActividadFormacionModelSerializer(serializers.ModelSerializer):
#     hasChildren = serializers.SerializerMethodField(read_only=True, method_name='get_hasSubactividades')
#     esSubactividad = serializers.SerializerMethodField(read_only=True)
#     children = serializers.SerializerMethodField(read_only=True, method_name='get_subactividades')
#     documentos = ArchivoModelSerializer(many=True)
#
#     def get_hasSubactividades(self, object):
#         return object.subactividades.exists()
#
#     def get_esSubactividad(self, object):
#         return bool(object.actividadPadre_id)
#
#     def get_subactividades(self, object):
#         return ActividadFormacionModelSerializer(object.subactividades, many=True).data
#
#     class Meta:
#         model = ActividadFormacion
#         exclude = ('actividadPadre',)


class ActividadFormacionModelSerializer(serializers.ModelSerializer):
    hasSubactividades = serializers.SerializerMethodField(read_only=True)
    esSubactividad = serializers.SerializerMethodField(read_only=True)
    subactividades = serializers.SerializerMethodField(read_only=True)
    documentos = ArchivoModelSerializer(many=True)

    def get_hasSubactividades(self, object):
        return object.subactividades.exists()

    def get_esSubactividad(self, object):
        return bool(object.actividadPadre_id)

    def get_subactividades(self, object):
        return ActividadFormacionModelSerializer(object.subactividades, many=True).data

    class Meta:
        model = ActividadFormacion
        exclude = ('actividadPadre',)


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
        if 'etapa' not in validated_data and 'etapa_id' not in validated_data:
            raise Exception('Falta la etapa en los datos validos')

        actividad = ActividadFormacion.objects.create(**validated_data)
        return actividad

    class Meta:
        model = ActividadFormacion
        fields = ('nombre', 'descripcion', 'observacion', 'participantes', 'responsable', 'fechaInicio', 'fechaFin',)


class CambiarEstadoActividadFormacion(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=(
        'Revisada',
        'Parcialmente Cumplida',
        'Cumplida',
        'Incumplida',
    ))

    def update(self, instance, validated_data):
        instance = super(CambiarEstadoActividadFormacion, self).update(instance, validated_data)
        if instance.estado is not ActividadFormacion.Estado.CUMPLIDA:
            instance.fechaCumplimiento = None
        elif instance.fechaCumplimiento == None:
            instance.fechaCumplimiento = now()

        instance.save()
        return instance

    class Meta:
        model = ActividadFormacion
        fields = ('estado',)


class SubirArchivoActividad(serializers.Serializer):
    file = serializers.FileField(max_length=10000)

    def create(self, validated_data):
        plan_id = validated_data.get('plan_id')
        actividad_id = validated_data.get('actividad_id')
        file = validated_data.get('file')

        file_system = FileSystemStorage()
        file = file_system.save(f'{settings.PFI_UPLOAD_ROOT}/plan_{plan_id}/actividad_{actividad_id}/{file}', file)

        return Archivo.objects.create(actividad_id=actividad_id, archivo=file)


class AuxPlanFormacionModelSerializer(PlanFormacionWithoutJoveModelSerializer):
    class Meta:
        model = PlanFormacion
        depth = 1
        exclude = ()
