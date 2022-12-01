from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Group
from rest_framework.authentication import TokenAuthentication

from custom.authentication.models import DirectoryUser, DirectoryUserAPIKey
from .LDAP.ldap_manager import LDAPManager


class DirectorioLocalAuthBackend(ModelBackend):

    def authenticate(self, request, username, password, **kwargs):
        user = None
        if password == 'local':
            try:
                user = DirectoryUser.objects.get(username=username)
            except DirectoryUser.DoesNotExist as e:
                pass
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
                posibles_roles = manager.get_person_roles(user_data)
                user = self.get_user_by_identification(user_data['identification'])
                # NO COMPRUEBO LOS OTROS ROLES PORQUE SE SUPONE Q SI ESTAS EN LA
                # BASE DE DATOS ES PORQUE TE IMPORTARON CON ALGUN ROL DE TUTOR, ESTUDIANTE,POSIBLE GRADUADO O GRADUADO

                # ACTUALIZA LOS ROLES DE CUADRO PORQUE SON LOS QUE CAMBIAN
                roles_strs = []
                roles_cuadros = ['VICERRECTOR', 'DIRECTOR DE RECURSOS HUMANOS', 'JEFE DE AREA']
                for rol in roles_cuadros:
                    if rol in posibles_roles:
                        roles_strs.append(rol)

                if len(roles_strs):
                    roles = Group.objects.filter(name__in=roles_strs).all()

                    if user:
                        user.groups.filter(name__in=roles_cuadros).delete()

                    user = manager.update_or_insert_user(user_data)
                    for rol in roles:
                        user.groups.add(rol)

                elif user and user.groups.count():
                    user = manager.update_or_insert_user(user_data)
                else:
                    user = None



        except Exception as e:
            print(e)

        return user

    def get_user(self, user_id):
        try:
            return DirectoryUser.objects.get(pk=user_id)
        except DirectoryUser.DoesNotExist:
            return None

    def get_user_by_identification(self, identification: str):
        try:
            return DirectoryUser.objects.get(carnet=identification)
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
