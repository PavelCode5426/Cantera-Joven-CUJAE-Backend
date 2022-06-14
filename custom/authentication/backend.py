from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import TokenAuthentication

from custom.authentication.directorio.autenticacion import Autenticacion
from . import directorio
from custom.authentication.models import DirectoryUser, DirectoryUserAPIKey

class DirectorioLocalAuthBackend(ModelBackend):

    def authenticate(self,request,username,password,**kwargs):
        user = None
        data = directorio.authenticate(username, password)
        if data:
            user = directorio.update_user(data['user'], data['permissions'])
        return user
    def get_user(self, user_id):
        try:
            return DirectoryUser.objects.get(pk=user_id)
        except DirectoryUser.DoesNotExist:
            return None

class DirectorioOnlineAuthBackend(ModelBackend):
    def authenticate(self,request,username,password,**kwargs):
        user = None
        data = None
        autentication = Autenticacion()

        try:
            data = autentication.authentication(username, password)
        except Exception:
            pass

        if data:
            user = autentication.update_or_insert_user(data)
        return user

    def get_user(self, user_id):
        try:
            return DirectoryUser.objects.get(pk=user_id)
        except DirectoryUser.DoesNotExist:
            return None


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'

class APIKeyAuthentication(TokenAuthentication):
    keyword = 'api-key'
    model = DirectoryUserAPIKey