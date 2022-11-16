from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import TokenAuthentication

from custom.authentication.models import DirectoryUser, DirectoryUserAPIKey
from .LDAP.ldap_manager import LDAPManager


class DirectorioLocalAuthBackend(ModelBackend):

    def authenticate(self, request, username, password, **kwargs):
        user = None
        if password == 'local':
            user = DirectoryUser.objects.get(username=username)
        return user

    def get_user(self, user_id):
        try:
            return DirectoryUser.objects.get(pk=user_id)
        except DirectoryUser.DoesNotExist:
            return None


class DirectorioOnlineAuthBackend(ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        user = None
        try:
            manager = LDAPManager()
            user_data = manager.authentication(username, password)

            if user_data:
                user = manager.update_or_insert_user(user_data)
        except Exception as e:
            print(e)

        return user

    def get_user(self, user_id):
        try:
            return DirectoryUser.objects.get(pk=user_id)
        except DirectoryUser.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        # IMPLEMENTAR PARA LOS ESTUDIANTE, POSIBLES GRADUADOS, GRADUADOS Y TUTORES
        return True


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class APIKeyAuthentication(TokenAuthentication):
    keyword = 'api-key'
    model = DirectoryUserAPIKey
