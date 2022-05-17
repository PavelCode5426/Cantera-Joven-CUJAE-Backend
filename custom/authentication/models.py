from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Permission, AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.

'''
MANAGER PARA USUARIOS, SON FUNCIONES QUE SIRVEN PARA MANIPULAR OBJETOS DE AUTH.MODELS.USER
'''
class CustomUserManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,username,directorioID):
        user = None
        if self.__validate_fields(first_name,last_name,email,directorioID):
            user = DirectoryUser()
            user.first_name = first_name
            user.last_name = last_name
            user.email = self.normalize_email(email)
            user.username = username
            user.directorioID = directorioID
            user.save()
        return user

    def create_superuser(self,first_name,last_name,email,username,directorioID):
        superUser = self.create_user(first_name,last_name,email,username,directorioID)
        superUser.is_superuser = True
        superUser.is_staff = True
        superUser.save()
        return superUser

    def __validate_fields(self,*args):
        for arg in args:
            if not arg:
                raise ValueError('Formulario Incompleto')

        return True



'''
CREANDO LAS BASES DE LOS USUARIO 
CON ELLO SE MODIFICA EL CREATESUPERUSER, LA CLASE USUARIO

USUARIO DEL DIRECTORIO DE LA CUJAE
'''
class DirectoryUser(AbstractUser): #Abstract User Implementa AbstractBaseUser,PermissionsMixin Juntos
    directorioID = models.CharField(max_length=255,blank=True)
    password = None #Eliminados por cuestion del directorio de la CUJAE

    objects=CustomUserManager()