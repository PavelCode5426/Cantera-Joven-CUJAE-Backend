from django.utils.timezone import now
from rest_framework import serializers
from core.base.models import modelosSimple,modelosPlanificacionFamiliarizarcion,modelosUsuario


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelosSimple.Area
        fields = '__all__'

class PreubicacionPosibleGraduadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelosUsuario.PosibleGraduado
        fields = ['id','first_name','last_name','email','direccion','directorioID']
class PreubicacionLaboralAdelantadaSerializer(serializers.ModelSerializer):
    posiblegraduado = PreubicacionPosibleGraduadoSerializer()

    def validate(self,data):

        ultima_area = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.\
            objects.filter(posiblegraduado=data.get('posiblegraduado'),esPreubicacion=False).order_by('-fechaAsignado')[:1]

        if ultima_area:
            raise serializers.ValidationError({'posiblegraduado':'El posible graduado no puede ser preubicado en su misma area'})

        return data
    def create(self, validated_data):
        posible_graduado = validated_data.get('posiblegraduado')
        preubicacion = None
        try:
            preubicacion = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.objects.get(posiblegraduado=posible_graduado,esPreubicacion=True)
            preubicacion.area = validated_data.get('area')
            preubicacion.fecha = now()

        except modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada.DoesNotExist:
            preubicacion = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada(**validated_data)

        finally:
            preubicacion.save()


        return preubicacion

    class Meta:
        model = modelosPlanificacionFamiliarizarcion.UbicacionLaboralAdelantada
        exclude = ['id','esPreubicacion']
        depth = 1



class SendNotificationSerializer(serializers.Serializer):
    mensaje = serializers.CharField()
    aceptada = serializers.BooleanField(required=True)