from django.utils.timezone import now
from rest_framework import serializers

from core.base.models import modelosSimple, modelosPlanificacionFamiliarizarcion, modelosUsuario


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelosSimple.Area
        exclude = ('distinguishedName',)


class PreubicacionLaboralAdelantadaSerializer(serializers.Serializer):
    posiblegraduado = serializers.PrimaryKeyRelatedField(required=True,
                                                         queryset=modelosUsuario.PosibleGraduado.objects.all())
    area = serializers.PrimaryKeyRelatedField(required=True, queryset=modelosSimple.Area.objects.all())

    def validate(self, data):
        ultima_area = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada. \
                          objects.filter(posiblegraduado_id=data.get('posiblegraduado'), esPreubicacion=False).order_by(
            '-fechaAsignado')[:1]

        if ultima_area:
            raise serializers.ValidationError(
                {'posiblegraduado': 'El posible graduado no puede ser preubicado en su misma area'})

        return data

    def create(self, validated_data):
        posible_graduado = validated_data.get('posiblegraduado')
        preubicacion = None
        try:
            preubicacion = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.objects.get(
                posiblegraduado=posible_graduado, esPreubicacion=True)
            preubicacion.area = validated_data.get('area')
            preubicacion.fecha = now()

        except modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.DoesNotExist:
            preubicacion = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada(**validated_data)

        finally:
            preubicacion.save()

        return preubicacion


class SendNotificationSerializer(serializers.Serializer):
    mensaje = serializers.CharField()
    aceptada = serializers.BooleanField(required=True)


class PosibleGraduadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelosUsuario.PosibleGraduado
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'direccion', 'lugarProcedencia')
        depth = 1


class PreubicacionLaboralAdelantadaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada
        exclude = ['posiblegraduado']
        depth = 1
