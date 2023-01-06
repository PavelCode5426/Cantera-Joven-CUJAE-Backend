from core.base.models.modelosUsuario import PlantillaAval
from . import seeder
from ..models.modelosSimple import PropuestaMovimiento, Dimension

seeder.add_entity(PlantillaAval, 5)
seeder.add_entity(PropuestaMovimiento, 10)
seeder.add_entity(Dimension, 10)
