from custom.authentication.directorio.estudiante import obtenerTodosEstudiantes
from core.base.models.modelosUsuario import Estudiante
from core.base.models.modelosSimple import Area
from core.configuracion.helpers import isConfigAvailable
from custom.logging import logger

@isConfigAvailable('auto_importar_estudiante')
def importar_estudiantes_automaticamente():
    estudiantes = obtenerTodosEstudiantes()
    for estudiante_dic in estudiantes:
        area = Area.objects.get_or_create(nombre=estudiante_dic['area'])[0] if 'area' in estudiante_dic else None
        data = dict(
            directorioID=estudiante_dic['id'],
            first_name=estudiante_dic['first_name'],
            last_name=estudiante_dic['last_name'],
            username=estudiante_dic['username'],
            email=estudiante_dic['email'],
            direccion=estudiante_dic['direccion'],
            anno_academico=estudiante_dic['anno'],
            area = area
        )
        Estudiante.objects.update_or_create(directorioID=data['directorioID'], defaults=data)
    logger.info('Estudiantes Importados Correctamente')