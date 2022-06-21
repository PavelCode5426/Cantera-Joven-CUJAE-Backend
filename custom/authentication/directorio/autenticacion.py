import requests

from core.base.models.modelosSimple import Area
from custom.authentication.models import DirectoryUser

DIRECTORIO_URL = 'http://apidev.cujae.edu.cu'
# DIRECTORIO_URL = 'http://apidevinter.cujae.edu.cu'

class Autenticacion:
    def authentication(self, username, password,**kwargs):
        user = None
        response = requests.get(DIRECTORIO_URL,headers={"Authorization":"Basic YWRtaW5pc3RyYXRvcjpncm91cGxkYXAyMDlxKis","x-access-token":""})

        if response.status_code == 200:
            pass #TODO Gestionar el response del Directorio Online

        return user
    def update_or_insert_user(self,userData):
        #TODO Falta que los datos del Directorio, borrar codigo, es de prueba
        if 'area' in userData:
            userData['area'] = Area.objects.get_or_create(nombre=userData['area'])[0]
            userData['directorioID'] = userData.pop('id')
        __user = DirectoryUser.objects.update_or_create(directorioID=userData['directorioID'], defaults=userData)[0]

        return __user