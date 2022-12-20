from core.configuracion.helpers import isConfigAvailable
from custom.logging import logger


@isConfigAvailable('mantener_actualizada_informacion_de_usuarios')
def actualizar_informacion_usuarios():
    # TODO LAURA AQUI HAZ EL CODIGO DE ACTUALIZAR LA INFORMACION DE LOS USUARIOS CON ROLES DE LA APP
    # EXCEPTO LOS ESTUDIANTES, POSIBLES GRADUADOS Y GRADUADOS POR UN TEMA DE RENDIMIENTO
    logger.info("Usuarios actualizados correctamente")
    pass
