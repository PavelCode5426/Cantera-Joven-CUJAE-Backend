from core.configuracion.helpers import isConfigAvailable
from custom.authentication.models import DirectoryUser
from custom.logging import logger

@isConfigAvailable('enviar_estado_notificaciones')
def enviar_estado_notificaciones_por_correo():
    usuarios = DirectoryUser.objects.distinct().filter(notifications__unread=True).all()
    for usuario in usuarios:
        cantidad_no_leidas = usuario.notifications.unread().count()
        #TODO Enviar correo electronico al usuario
    logger.info('Correos con estado de notificaciones enviados correctamente')