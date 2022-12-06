from rest_framework import serializers

from core.base.models.modelosPlanificacion import Evaluacion
from core.base.models.modelosPlanificacionFormacion import PlanFormacionComplementaria, EtapaFormacion
from core.base.validators import datetime_greater_now
from core.formacion_complementaria.base.serializers import GraduadoSerializer
from custom.authentication.serializer import DirectoryUserSerializer


class EvaluacionModelSerializer(serializers.ModelSerializer):
    aprobadoPor = DirectoryUserSerializer(allow_null=True)

    class Meta:
        model = Evaluacion
        exclude = ()


class CrearEvaluacionModelSerializer(serializers.ModelSerializer):
    esSatisfactorio = serializers.BooleanField()

    class Meta:
        model = Evaluacion
        exclude = ('aprobadoPor',)


class EtapaFormacionModelSerializer(serializers.ModelSerializer):
    numero = serializers.IntegerField(read_only=True)
    esProrroga = serializers.BooleanField(read_only=True)
    evaluacion = EvaluacionModelSerializer(allow_null=True, read_only=True)

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


class PlanFormacionComplementariaModelSerializer(serializers.ModelSerializer):
    graduado = GraduadoSerializer(read_only=True)
    # etapas = EtapaFormacionModelSerializer(many=True, read_only=True)
    aprobadoPor = DirectoryUserSerializer(allow_null=True, read_only=True)

    class Meta:
        model = PlanFormacionComplementaria
        depth = 1
        exclude = ()
