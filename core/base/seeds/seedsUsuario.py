import random

from custom.authentication.models import DirectoryUser
from . import seeder
from ..models.modelosSimple import Area
from ..models.modelosUsuario import Estudiante, Graduado


def fake_data_func_user():
    def random_dni():
        dni = ''
        for i in range(0, 11):
            dni += str(random.randint(0, 9))
        return dni

    return {
        'area': lambda x: Area.objects.order_by('?').first(),
        'is_superuser': False,
        'is_staff': False,
        'direccion': lambda x: seeder.faker.address(),
        'carnet': lambda x: random_dni(),
        'telefono': lambda x: seeder.faker.phone_number()
    }


def fake_data_func_estudiante():
    result = fake_data_func_user()
    result.pop('area')
    return {**result, 'anno_academico': lambda x: random.randint(1, 5)}


# CREAR USUARIO DE FIJO EN EL SISTEMA

try:
    user = DirectoryUser.objects.create_superuser("Administrador", "Administrador",
                                                  "admin@ceis.cujae.edu.cu",
                                                  "admin")

    user.area = Area.objects.get(nombre='Facultad de Ingenieria Informatica')
    user.save()
except Exception:
    pass

seeder.add_entity(DirectoryUser, 100, fake_data_func_user())

seeder.add_entity(Graduado, 100, fake_data_func_user())

seeder.add_entity(Estudiante, 50, fake_data_func_estudiante())
