from django.utils.timezone import now
from rest_framework import serializers


def datetime_greater_now(value):
    if value < now():
        raise serializers.ValidationError('La fecha no puede ser menor que hoy')
    return value
