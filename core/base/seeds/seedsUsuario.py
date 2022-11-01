import random

from core.base.models import modelosSimple
from core.base.models import modelosUsuario
from custom.authentication import models as authModels
from . import seeder

fake_data = {
    'area': lambda x: modelosSimple.Area.objects.order_by('?').first(),
    'is_superuser': False,
    'is_staff': False,
    'direccion': lambda x: seeder.faker.address(),
    'directorioID': lambda x: random.randint(50, 1000)
}
seeder.add_entity(authModels.DirectoryUser, 20, fake_data)

# Me daba error si volvia a asignar la variables y asi funciona.
fake_data_1 = dict(**fake_data)
seeder.add_entity(modelosUsuario.Graduado, 10, fake_data_1)

fake_data_2 = dict(**fake_data,
                   **{'lugarProcedencia': lambda x: modelosSimple.LugarProcedencia.objects.order_by('?').first()})
fake_data_2.pop('area')
seeder.add_entity(modelosUsuario.PosibleGraduado, 5, fake_data_2)

fake_data_3 = dict(**fake_data, **{'anno_academico': lambda x: random.randint(1, 5)})
fake_data_3.pop('area')
seeder.add_entity(modelosUsuario.Estudiante, 5, fake_data_3)

fake_data = {
    'usuario': lambda x: modelosUsuario.Graduado.objects.filter(aval=None).order_by('?').first()
}
seeder.add_entity(modelosUsuario.Aval, 5, fake_data)
