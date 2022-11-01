from notifications.models import Notification
from notifications.signals import notify
from rest_framework import serializers

from custom.authentication.models import DirectoryUser
from custom.authentication.serializer import DirectoryUserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField('get_sender')

    def get_sender(self, obj):
        return DirectoryUserSerializer(obj.actor).data

    class Meta:
        model = Notification
        fields = ['id', 'level', 'verb', 'description', 'data', 'unread', 'timestamp', 'sender']
        depth = 1


class EnviarNotificacionMasivaSerializer(serializers.Serializer):
    texto = serializers.CharField(required=True)

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if is_valid:
            sender = self.context['sender']
            self._validated_data['usuarios'] = DirectoryUser.objects.exclude(pk=sender.pk).all()
        return is_valid

    def create(self, validated_data):
        sender = self.context['sender']
        texto = validated_data['texto']
        usuarios = validated_data['usuarios']
        notify.send(sender, recipient=usuarios, verb=texto, data={})


class EnviarNotificacionSerializer(EnviarNotificacionMasivaSerializer):
    usuarios = serializers.PrimaryKeyRelatedField(many=True, queryset=DirectoryUser.objects.all(), required=True,
                                                  allow_empty=False)

    def is_valid(self, raise_exception=False):
        return super(serializers.Serializer, self).is_valid(raise_exception)
