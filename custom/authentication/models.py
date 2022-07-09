import binascii
import os

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Permission, AbstractUser, PermissionsMixin
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
    area = models.ForeignKey("base.Area",on_delete=models.RESTRICT,null=True,blank=True)
    direccion = models.CharField(max_length=255,blank=True)
    directorioID = models.CharField(max_length=255,blank=True)
    password = None #Eliminados por cuestion del directorio de la CUJAE
    roles = []

    objects=CustomUserManager()

class APIKeyManager(models.Manager):
    def create_apikey(self,user:DirectoryUser,name='default',expire_in=None):
        apiKey=DirectoryUserAPIKey(
            user=user,
            name = name,
            expired_at = expire_in
        ).save()

        return apiKey

class DirectoryUserAPIKey(models.Model):
    key = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(DirectoryUser,models.CASCADE)
    is_active = models.BooleanField(default=True)
    expired_at = models.DateTimeField(blank=True,null=True,default=None)
    created_at = models.DateTimeField(auto_now=True)

    objects = APIKeyManager()

    def save(self,*args,**kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode()
        return super(DirectoryUserAPIKey,self).save(*args,**kwargs)

    def __str__(self):
        return self.name+' '+self.user.username

    class Meta:
        verbose_name = 'API-Key'
        verbose_name_plural = 'API-Keys'

