from rest_framework import serializers
from core.base.models import modelosSimple


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelosSimple.Area
        fields = '__all__'