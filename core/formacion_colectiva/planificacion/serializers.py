import os

from crum import get_current_request
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers

from config import settings
from core.base.models.modelosPlanificacion import Plan, Archivo, Etapa, Comentario, Evaluacion
from core.base.models.modelosPlanificacionColectiva import ActividadColectiva
from core.base.models.modelosUsuario import PosibleGraduado
from core.base.validators import datetime_greater_now
from core.formacion_colectiva.gestionar_area.serializers import AreaSerializer
from custom.authentication.serializer import DirectoryUserSerializer


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


class PlanFormacionColectivaModelSerializer(serializers.ModelSerializer):
    documento = serializers.SerializerMethodField(method_name='last_version', read_only=True, allow_null=True)

    def last_version(self, obj):
        archivo = obj.versiones.order_by('-fecha').first()
        if archivo:
            return ArchivoModelSerializer(instance=archivo, context=self.context).data
        return None

    class Meta:
        model = Plan
        exclude = ()


class UpdateEstadoPlanFormacionColectivoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=(
        'En Desarrollo',
        'Pendiente de Revision'
    ))

    class Meta:
        model = Plan
        fields = ('estado',)


class EtapaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapa
        exclude = ()


class UpdateEtapaColectivaSerializer(EtapaModelSerializer):
    fechaInicio = serializers.DateTimeField(validators=[datetime_greater_now])
    fechaFin = serializers.DateTimeField(validators=[datetime_greater_now])

    def is_valid(self, raise_exception=False):
        super(UpdateEtapaColectivaSerializer, self).is_valid(True)

        valid = self._validated_data

        if valid['fechaInicio'] > valid['fechaFin']:
            self._errors.setdefault('fechaInicio', ['Fecha mayor que la de fin'])
            self._errors.setdefault('fechaFin', ['Fecha menos que la de inicio'])

        return super(UpdateEtapaColectivaSerializer, self).is_valid(True)

    class Meta:
        model = Etapa
        exclude = ('plan',)


class CommentsModelSerializer(serializers.ModelSerializer):
    texto = serializers.CharField()
    usuario = DirectoryUserSerializer(read_only=True, required=False)

    def is_valid(self, raise_exception=False):
        super(CommentsModelSerializer, self).is_valid(raise_exception)

        view_kwargs: dict = self.context['view'].kwargs
        request = self.context['request']

        self._validated_data.setdefault('plan_id', view_kwargs.get('planID', None))
        self._validated_data.setdefault('usuario', request.user)

        return super(CommentsModelSerializer, self).is_valid(raise_exception)

    class Meta:
        model = Comentario
        exclude = ('plan', 'actividad')


class ActividadColectivaModelSerializer(serializers.ModelSerializer):
    documentos = ArchivoModelSerializer(many=True)

    class Meta:
        model = ActividadColectiva
        exclude = ('actividadPadre', 'area', 'asistencias',)


class ActividadColectivaAreaModelSerializer(ActividadColectivaModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = ActividadColectiva
        exclude = ('actividadPadre', 'asistencias',)


class CreateUpdateActividadColectivaSerializer(serializers.ModelSerializer):
    fechaInicio = serializers.DateTimeField(validators=[datetime_greater_now])

    def create(self, validated_data: dict):
        if 'etapa' not in validated_data and 'etapa_id' not in validated_data:
            raise Exception('Falta la etapa en los datos validos')

        actividad = ActividadColectiva.objects.create(**validated_data)
        return actividad

    class Meta:
        model = ActividadColectiva
        exclude = ('area', 'actividadPadre', 'asistencias', 'etapa',)


class CreateUpdateActividadAreaSerializer(CreateUpdateActividadColectivaSerializer):
    def create(self, validated_data: dict):
        if 'etapa' not in validated_data and 'etapa_id' not in validated_data:
            raise Exception('Falta la etapa en los datos validos')

        if 'actividadPadre' not in validated_data and 'actividadPadre_id' not in validated_data:
            raise Exception('Falta la actividadPadre en los datos validos')

        if 'area' not in validated_data and 'area_id' not in validated_data:
            raise Exception('Falta la actividadPadre en los datos validos')

        validated_data['esGeneral'] = False
        actividad = ActividadColectiva.objects.create(**validated_data)
        return actividad

    class Meta:
        model = ActividadColectiva
        exclude = ('asistencias', 'etapa', 'actividadPadre')


class FirmarPlanColectivoSerializer(serializers.Serializer):
    sign = serializers.BooleanField()
    file = serializers.FileField(required=False)

    def is_valid(self, raise_exception=False):
        super(FirmarPlanColectivoSerializer, self).is_valid(raise_exception)

        validated_data = self._validated_data
        if validated_data.get('sign') and not validated_data.get('file', None):
            self._errors['file'] = [self.error_messages['required']]

        return super(FirmarPlanColectivoSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        plan: Plan = validated_data.get('plan')
        if not validated_data.get('sign'):
            plan.estado = plan.Estados.RECHAZADO
        else:
            plan.estado = plan.Estados.APROBADO
            plan.aprobadoPor = validated_data.get('user')
            file = validated_data.get('file')

            extension = os.path.splitext(file.name)[1]
            version = plan.versiones.count() + 1
            file_system = FileSystemStorage()
            file = file_system.save(f'{settings.PFC_UPLOAD_ROOT}/plan_{plan.pk}/v_{version}{extension}', file)

            plan.versiones.create(plan_id=plan.pk, archivo=file)

        plan.save()
        return validated_data['sign']


class SubirArchivoActividad(serializers.Serializer):
    file = serializers.FileField(max_length=10000)

    def create(self, validated_data):
        plan_id = validated_data.get('plan_id')
        actividad_id = validated_data.get('actividad_id')
        file = validated_data.get('file')

        file_system = FileSystemStorage()
        file = file_system.save(f'{settings.PFC_UPLOAD_ROOT}/plan_{plan_id}/actividad_{actividad_id}/{file}', file)

        return Archivo.objects.create(actividad_id=actividad_id, archivo=file)


class ActividadAsistenciaSerilizer(serializers.ModelSerializer):
    asistencias = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=PosibleGraduado.objects.filter(evaluacion=None).all()),
        allow_empty=True
    )

    def is_valid(self, raise_exception=False):
        super(ActividadAsistenciaSerilizer, self).is_valid(raise_exception)

        area = self.context.get('request').user.area
        jovenes = self._validated_data.get('asistencias')

        found = False
        it = iter(jovenes)
        try:
            while not found:
                elem = next(it)
                if elem.area_id is not area.pk:
                    found = True
        except StopIteration:
            pass

        if found:
            self._errors.setdefault('jovenes', ['Ha seleccionado jovenes inexistentes en su area'])

        return super(ActividadAsistenciaSerilizer, self).is_valid(raise_exception)

    def update(self, instance, validated_data):
        area = self.context.get('request').user.area
        jovenes_area = PosibleGraduado.objects.filter(area=area, evaluacion=None).all()
        for joven in jovenes_area:
            instance.asistencias.remove(joven)
        return super(ActividadAsistenciaSerilizer, self).update(instance, validated_data)

    class Meta:
        model = ActividadColectiva
        fields = ('asistencias',)


class EvaluacionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        exclude = ()
