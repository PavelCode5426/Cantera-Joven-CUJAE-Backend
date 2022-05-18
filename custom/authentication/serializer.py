from crum import get_current_user
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _

from .models import DirectoryUser,DirectoryUserAPIKey


class CustomAuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = {'detail':_('Unable to log in with provided credentials.')}
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = {'detail':_('Must include "username" and "password".')}
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class DirectoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectoryUser
        fields = ('id','username','first_name','last_name','email')


class DirectoryUserAPIKeySerializer(serializers.ModelSerializer):
    key = serializers.CharField(required=False)
    def create(self, validated_data):
        validated_data['user']=get_current_user()
        return super().create(validated_data)

    class Meta:
        model = DirectoryUserAPIKey
        fields = ('id','name','key','expired_at')