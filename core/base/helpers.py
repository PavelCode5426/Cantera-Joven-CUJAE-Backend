def notificar_al_DRH(mensaje):
    pass


from django.db import connections
from django.db.migrations.executor import MigrationExecutor


def is_database_synchronized(database):
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)
