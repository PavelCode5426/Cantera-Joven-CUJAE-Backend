from custom.authentication.models import DirectoryUser
from custom.authentication.directorio import obtenerUsuariosPorIDs,update_user
from custom.logging import logger
from core.configuracion.helpers import isConfigAvailable

@isConfigAvailable('auto_actualizar_usuario')
def actualizar_informacion_usuarios():
    usuarios = DirectoryUser.objects.all()
    ids = [usuario.pk for usuario in usuarios]
    usuarios_directorio = obtenerUsuariosPorIDs(ids)

    for usuario_dir in usuarios_directorio:
        if 'password' in usuario_dir:
            usuario_dir.pop('password')
        update_user(usuario_dir)
    logger.info("Usuarios actualizados correctamente")