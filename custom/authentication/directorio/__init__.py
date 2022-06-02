from custom.authentication.models import DirectoryUser

_usuarios = [
    {'id':1,'email':'perezpavel5426@gmail.com','username':'pperez','password':'1234','first_name':'Pavel','last_name':'Perez Gonzalez'},
    {'id':2,'email':'lauramendezdelpino@gmail.com','username':'laura','password':'1234','first_name':'Laura','last_name':'Mendez del Pino'},
]


def authenticate(username,password):
    find = None
    raise Exception('asdasdasd')
    count = 0
    while find is None and count < len(_usuarios):
        if _usuarios[count]['username'] == username and _usuarios[count]['password'] == password:
            find = {'user':_usuarios[count],'permissions':[]}
        count+=1
    return find


#Auxiliar
def update_user(user,permissions=[]):
    __user = None
    try:
        __user = DirectoryUser.objects.get(directorioID=user['id'])
    except DirectoryUser.DoesNotExist:
        __user = DirectoryUser()
        __user.directorioID = user['id']

    __user.email = user['email']
    __user.username = user['username']
    __user.first_name = user['first_name']
    __user.last_name = user['last_name']
    __user.save()

    #TODO Cargar los permisos del Usuario

    return __user