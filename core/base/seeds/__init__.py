from django_seed import Seed

seeder = Seed.seeder()

def executeSeeds():
    from . import seedsSimple
    from . import seedsUsuario
    from . import seedsTutoria
    from . import seedsPlanificacion
    from . import seedsPlanificacionCantera
    from . import seedsPlanificacionFamiliarizarcion
    from . import seedsPlanificacionFormacionComplementaria
    seeder.execute()

execute = executeSeeds
