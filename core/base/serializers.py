from rest_framework import serializers


class ImportarFromDirectorioSerializer(serializers.Serializer):
    importar = serializers.ListField(child=serializers.CharField(max_length=11, min_length=11))
