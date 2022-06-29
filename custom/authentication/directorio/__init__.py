from custom.authentication.models import DirectoryUser
from core.base.models.modelosSimple import Area

_usuarios = [
    {'id':1,'email':'perezpavel5426@gmailm.com','username':'pperez','password':'1234','first_name':'Pavel','last_name':'Perez Gonzalez','area':'Informatica'},
    {'id':2,'email':'lauramendezdelpino@gmail.commm','username':'laura','password':'1234','first_name':'Laura','last_name':'Mendez del Pino','area':'Informatica'},
    {'id':3,'email':'aramays@gmail.commm','username':'ara','password':'1234','first_name':'Aramays','last_name':'Morales Duran','area':'Civil'},
    {'id':4,'email':'monik@gmail.commm','username':'mony','password':'1234','first_name':'Monik','last_name':'Montoto Montene','area':'Civil'},
]

def authenticate(username,password):
    find = None
    count = 0
    while find is None and count < len(_usuarios):
        if _usuarios[count]['username'] == username and _usuarios[count]['password'] == password:
            find = {'user':{**_usuarios[count]},'permissions':[]}
            find['user'].pop('password')
        count+=1
    return find

#Auxiliar
def update_or_create_user(userData, permissions=[]):
    __user = None
    userData['area'] = Area.objects.get_or_create(nombre=userData['area'])[0] if 'area' in userData else None
    userData['directorioID'] = userData.pop('id')
    userData['email'] = DirectoryUser.objects.normalize_email(userData['email'])
    __user = DirectoryUser.objects.update_or_create(directorioID=userData['directorioID'], defaults=userData)[0]
    return __user

def update_user(userData,permissions=[]):
    userData['area'] = Area.objects.get_or_create(nombre=userData['area'])[0] if 'area' in userData else None
    userData['directorioID'] = userData.pop('id')
    userData['email'] = DirectoryUser.objects.normalize_email(userData['email'])
    user = DirectoryUser.objects.filter(directorioID=userData['directorioID']).update(**userData)
    return user

def obtenerUsuariosPorIDs(ids=[]):
    return obtenerPorIDs(_usuarios.copy(),ids)

class ItemNotFoundException(Exception):
    pass

def obtenerPorID(list,id):
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

def obtenerPorIDs(lis,listIDs=[]):
    if not len(listIDs):
        return listIDs
    else:
        items = list()
        for id in listIDs:
            elem = obtenerPorID(lis,id)
            if elem: items.append(elem)
            #else: raise ItemNotFoundException()
        return items.copy()

