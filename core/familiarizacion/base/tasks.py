# @isConfigAvailable('auto_importar_posible_graduado')
# def importar_posibles_graduados_automaticamente():
#     posiblesGraduados = obtenerPosibleGraduados()
#     for posibleGraduado in posiblesGraduados:
#         lugarProcedencia = LugarProcedencia.objects.get_or_create(nombre=posibleGraduado['lugarProcedencia'])[0] if 'lugarProcedencia' in posibleGraduado else None
#         data = dict(
#             directorioID=posibleGraduado['id'],
#             first_name=posibleGraduado['first_name'],
#             last_name=posibleGraduado['last_name'],
#             username=posibleGraduado['username'],
#             email=posibleGraduado['email'],
#             direccion=posibleGraduado['direccion'],
#             lugarProcedencia=lugarProcedencia
#         )
#         PosibleGraduado.objects.update_or_create(directorioID=data['directorioID'], defaults=data)
#     logger.info('Posibles Graduados Importados Correctamente')
