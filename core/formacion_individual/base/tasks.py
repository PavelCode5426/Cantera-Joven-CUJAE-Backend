from core.configuracion.helpers import isConfigAvailable
from custom.logging import logger


@isConfigAvailable('mantener_actualizada_informacion_de_graduados')
def actualizar_informacion_graduados():
    # TODO LAURA HAZ ESTO AVISAME CUANDO VAYAS X AQUI
    logger.critical('Graduados actualizados correctamente')


@isConfigAvailable('mantener_actualizada_informacion_de_estudiantes')
def actualizar_informacion_estudiantes():
    # TODO LAURA HAZ ESTO AVISAME CUANDO VAYAS X AQUI
    logger.critical('Estudiantes actualizados correctamente')
