from django_seed import Seed

seeder = Seed.seeder()


def executeSeeds():
    from . import seedsSoporte
    from . import seedsUsuario
    from . import seedsPlanificacion
    from . import seedsNotificacion

    seeder.execute()


execute = executeSeeds
