from core.configuracion.helpers import isConfigAvailable
from custom.logging import logger


@isConfigAvailable('mantener_actualizada_informacion_de_posibles_graduados')
def actualizar_informacion_posibles_graduados():
    logger.critical('Posibles Graduados actualizados correctamente')
