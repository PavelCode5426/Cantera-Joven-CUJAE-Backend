from rest_framework import serializers

from core.base.models import modelosUsuario
from core.formacion_complementaria.gestionar_avales.exceptions import UserAlreadyHaveAvalException


class UserAvalSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid()
        if is_valid and not self.instance:
            self._validated_data['usuario'] = self.initial_data['usuario']
            if modelosUsuario.Aval.objects.filter(usuario=self.initial_data.get('usuario')).exists():
                is_valid = False
                raise UserAlreadyHaveAvalException
                # self._errors.setdefault('detail','El usuario ya presenta un aval')

        return is_valid

    class Meta:
        model = modelosUsuario.Aval
        exclude = ('id', 'usuario')


class PlantillaAvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelosUsuario.PlantillaAval
        fields = '__all__'
