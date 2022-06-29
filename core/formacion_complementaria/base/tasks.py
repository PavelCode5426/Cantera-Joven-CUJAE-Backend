from custom.authentication.directorio.graduado import obtenerTodosGraduados
from core.base.models.modelosUsuario import Graduado
from core.base.models.modelosSimple import Area
from core.configuracion.helpers import isConfigAvailable
from custom.logging import logger

@isConfigAvailable('auto_importar_graduado')
def importar_graduados_automaticamente():
    graduados = obtenerTodosGraduados()
    for graduado in graduados:
        area = Area.objects.get_or_create(nombre=graduado['area'])[0] if 'area' in graduado else None
        data = dict(
            directorioID=graduado['id'],
            first_name=graduado['first_name'],
            last_name=graduado['last_name'],
            username=graduado['username'],
            email=graduado['email'],
            direccion=graduado['direccion'],
            area=area
        )
        Graduado.objects.update_or_create(directorioID=data['directorioID'], defaults=data)
    logger.info('Graduados Importados Correctamente')