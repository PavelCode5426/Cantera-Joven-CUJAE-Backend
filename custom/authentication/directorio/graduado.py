__graduados = [
    {'id': 175, 'email': 'estudiante33@gmail.com', 'username': 'roma', 'first_name': 'Roma', 'last_name': 'Was','direccion': 'Ave 31 Calle 50',
     'area':'Informatica','esExterno':True,'esNivelSuperior':True},
    {'id': 982, 'email': 'estudiante4@gmail.com', 'username': 'mateov', 'first_name': 'Mateo', 'last_name': 'Vita',
     'direccion': 'Guanabo #6565',
     'area':'Civil','esExterno':False,'esNivelSuperior':False},
    {'id':544,'email':'estudiante707@gmail.com','username':'trumrachel','first_name':'Rachel','last_name':'Trum','direccion':'Calle 100 #1105',
     'area':'Mantenimiento','esExterno': True, 'esNivelSuperior': False},
    {'id':333,'email':'estudiante6@gmail.com','username':'enr','first_name':'Enrique','last_name':'Gonzalez','direccion':'Ave Boyeros #3434',
     'area':'Informatica','esExterno':True, 'esNivelSuperior': True},
    {'id':230,'email':'estudiante5@gmail.com','username':'alfred','first_name':'Ramon','last_name':'Alfred','direccion':'Calle Azul #4565',
     'area':'Informatica','esExterno': False, 'esNivelSuperior': True},

]


def obtenerGraduado(id):
    from . import obtenerPorID
    return obtenerPorID(__graduados, id)

def obtenerGraduados(listIDs=[]):
    from . import obtenerPorIDs
    return obtenerPorIDs(__graduados, listIDs)

def obtenerTodosGraduados():
    return __graduados





