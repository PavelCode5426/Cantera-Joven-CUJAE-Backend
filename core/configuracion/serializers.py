from rest_framework.serializers import ModelSerializer
from core.base.models import modelosSimple

class ConfigurationSerializer(ModelSerializer):
    class Meta:
        model = modelosSimple.Configuracion
        fields = '__all__'