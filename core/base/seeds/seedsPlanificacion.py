from . import seeder
from ..models.modelosPlanificacionIndividual import TutoresAsignados
from ..models.modelosUsuario import Aval, Graduado

fake_data_aval = {
    'usuario': lambda x: Graduado.objects.filter(aval=None).order_by('?').first()
}
seeder.add_entity(Aval, 50, fake_data_aval)
seeder.add_entity(TutoresAsignados, 50)
