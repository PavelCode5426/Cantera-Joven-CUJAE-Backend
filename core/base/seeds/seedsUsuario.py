import random

from core.base.models import modelosSimple
from core.base.models import modelosUsuario
from custom.authentication import models as authModels
from . import seeder


def fake_data_func_user():
    def random_dni():
        dni = ''
        for i in range(0, 11):
            dni += str(random.randint(0, 9))
        return dni

    return {
        'area': lambda x: modelosSimple.Area.objects.order_by('?').first(),
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


fake_data_aval = {
    'usuario': lambda x: modelosUsuario.Graduado.objects.filter(aval=None).order_by('?').first()
}

# CREAR USUARIO DE FIJO EN EL SISTEMA

authModels.DirectoryUser.objects.create_superuser("Administrador", "Administrador", "admin@ceis.cujae.edu.cu", "admin")

# seeder.add_entity(authModels.DirectoryUser, 100, fake_data_func_user())

# seeder.add_entity(modelosUsuario.Graduado, 100, fake_data_func_user())

# seeder.add_entity(modelosUsuario.Estudiante, 50, fake_data_func_estudiante())

# seeder.add_entity(modelosUsuario.Aval, 50, fake_data_aval)

seeder.add_entity(modelosUsuario.PlantillaAval, 5)
