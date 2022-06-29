from rest_framework import serializers
from notifications.models import Notification
from notifications.signals import notify

from custom.authentication.models import DirectoryUser


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        #fields = ['id','level','verb','description','data','timestamp']
        fields = '__all__' #TODO Cambiar esto por el de arriba

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
        notify.send(sender, recipient=usuarios, verb=texto,data={'hola':True})

class EnviarNotificacionSerializer(EnviarNotificacionMasivaSerializer):
    usuarios = serializers.PrimaryKeyRelatedField(many=True,queryset=DirectoryUser.objects.all(),required=True,allow_empty=False)

    def is_valid(self, raise_exception=False):
        return super(serializers.Serializer,self).is_valid(raise_exception)