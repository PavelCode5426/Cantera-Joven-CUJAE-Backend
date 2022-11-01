from django.contrib.auth.models import Group

from core.base.models.modelosSimple import Area
from custom.authentication.models import DirectoryUser

_usuarios = [
    {'id': 1, 'email': 'perezpavel5426@gmailm.com', 'username': 'pperez', 'password': '1234', 'first_name': 'Pavel',
     'last_name': 'Perez Gonzalez', 'area': 'Informatica', 'roles': ['Jefe de Area']},
    {'id': 2, 'email': 'lauramendezdelpino@gmail.commm', 'username': 'laura', 'password': '1234', 'first_name': 'Laura',
     'last_name': 'Mendez del Pino', 'area': 'Informatica', 'roles': []},
    {'id': 3, 'email': 'aramays@gmail.commm', 'username': 'ara', 'password': '1234', 'first_name': 'Aramays',
     'last_name': 'Morales Duran', 'area': 'Civil', 'roles': []},
    {'id': 4, 'email': 'monik@gmail.commm', 'username': 'mony', 'password': '1234', 'first_name': 'Monik',
     'last_name': 'Montoto Montene', 'area': 'Civil', 'roles': []},
]


def authenticate(username, password):
    find = None
    count = 0
    while find is None and count < len(_usuarios):
        if _usuarios[count]['username'] == username and _usuarios[count]['password'] == password:
            find = {**_usuarios[count]}
            find.pop('password')
        count += 1
    return find


# Auxiliar
def update_or_create_user(userData):
    __user = None
    __roles = userData.pop('roles')

    userData['area'] = Area.objects.get_or_create(nombre=userData['area'])[0] if 'area' in userData else None
    userData['directorioID'] = userData.pop('id')
    userData['email'] = DirectoryUser.objects.normalize_email(userData['email'])
    __user, created = DirectoryUser.objects.update_or_create(userData, directorioID=userData['directorioID'])

    __user.groups.all().delete()
    for role in __roles:
        role, created = Group.objects.get_or_create({'name': role}, name=role)
        __user.groups.add(role)

    return __user


def update_user(userData):
    userData['area'] = Area.objects.get_or_create(nombre=userData['area'])[0] if 'area' in userData else None
    userData['directorioID'] = userData.pop('id')
    userData['email'] = DirectoryUser.objects.normalize_email(userData['email'])
    user = DirectoryUser.objects.filter(directorioID=userData['directorioID']).update(**userData)
    return user


def obtenerUsuariosPorIDs(ids=[]):
    return obtenerPorIDs(_usuarios.copy(), ids)


class ItemNotFoundException(Exception):
    pass


def obtenerPorID(list, id):
    encontrado = False
    item = None
    it = iter(list)
    while not encontrado:
        try:
            elem = next(it)
            if elem['id'] == id:
                item = dict(**elem)
                encontrado = True
        except StopIteration:
            encontrado = True

    return item


def obtenerPorIDs(lis, listIDs=[]):
    if not len(listIDs):
        return listIDs
    else:
        items = list()
        for id in listIDs:
            elem = obtenerPorID(lis, id)
            if elem: items.append(elem)
            # else: raise ItemNotFoundException()
        return items.copy()
