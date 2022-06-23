__estudiantes = [
    {'id': 100, 'email': 'estudiante_106@gmail.com', 'username': 'rdorsey', 'first_name': 'Raymond',
     'last_name': 'Dorsey', 'direccion': 'La Habana 105', 'anno': 1, 'area': 'Informatica'},
    {'id': 101, 'email': 'estudiante_105@gmail.com', 'username': 'lily10', 'first_name': 'Lili', 'last_name': 'Dorsey',
     'direccion': 'Ave 3ra #100', 'anno': 3, 'area': 'Economia'},
    {'id': 199, 'email': 'estudiante_104@gmail.com', 'username': 'est01', 'first_name': 'Rose', 'last_name': 'Call',
     'direccion': 'La Habana 70989', 'anno': 4, 'area': 'Mantenimiento'},
    {'id': 182, 'email': 'estudiante_103@gmail.com', 'username': 'est2010', 'first_name': 'Loren',
     'last_name': 'Hernandez', 'direccion': 'Ave 51 Calle 88', 'anno': 2, 'area': 'Informatica'},
    {'id': 343, 'email': 'estudiante_102@gmail.com', 'username': 'lemuspepe', 'first_name': 'Pepe',
     'last_name': 'Lemus', 'direccion': 'Ave 42 #4556', 'anno': 1, 'area': 'Informatica'},
]


def obtenerEstudiante(id):
    from . import obtenerPorID
    return obtenerPorID(__estudiantes, id)


def obtenerEstudiantes(listIDs=[]):
    from . import obtenerPorIDs
    return obtenerPorIDs(__estudiantes, listIDs)


def obtenerPorAnno(__estudiantes, anno):
    items = list()
    it = iter(__estudiantes)
    lenght = len(__estudiantes)

    while lenght > 0:
        elem = next(it)
        if elem['anno'] == anno:
            items.extend(elem)
    return items


def obtenerTodosEstudiantes():
    return __estudiantes
