from rest_framework import serializers
from django.contrib.admin.models import LogEntry

class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        exclude = ['user']
        depth = 1