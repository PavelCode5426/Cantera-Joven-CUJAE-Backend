from core.base.models.modelosSimple import Area
from custom.authentication.LDAP.sigenu_ldap import SIGENU_LDAP, SearchOption
from custom.authentication.models import DirectoryUser


class LDAPManager:

    def __init__(self):
        self.sigenu_ldap = SIGENU_LDAP()

    def authentication(self, username, password):
        user = None
        response = SIGENU_LDAP().login(username, password)

        if response.status_code == 200:
            user = response.json()

        return user

    def search_by_dni(self, dni: str):
        user = self.sigenu_ldap.search_all(SearchOption(identification=dni)).json()
        user = None if len(user) == 0 else user[0]
        area = None
        if user:
            try:
                area = Area.objects.get(nombre=user['area'])
            except Area.DoesNotExist as e:
                areas = self.sigenu_ldap.areas().json()
                for a in areas:
                    Area.objects.update_or_create(
                        defaults=dict(
                            nombre=a['name'],
                            distinguishedName=a['distinguishedName']
                        ), nombre=a['name'])

                area = Area.objects.get(nombre=user['area'])

            persons = self.sigenu_ldap.persons_by_area(area.distinguishedName).json()

            def filter_function(value):
                return dni == value['cUJAEPersonDNI']

            user = list(filter(filter_function, persons))
            user = user[0] if len(user) else None

        return (user, area)

    def update_or_insert_user(self, userData: dict):
        # TODO Falta que los datos del Directorio, borrar codigo, es de prueba
        user, area = self.search_by_dni(userData['identification'])

        if user and userData:
            userData = dict(
                first_name=user['givenName'],
                last_name=user['sn'],
                direccion=user['streetAddress'],
                cargo=None if 'title' not in user else user['title'],
                carnet=user['cUJAEPersonDNI'],
                directorioID=user['distinguishedName'],
                telefono=user['telephoneNumber'],
                email=user['mail'],
                username=user['sAMAccountName'],
                area=area
            )

        __user = DirectoryUser.objects.update_or_create(directorioID=userData['directorioID'], defaults=userData)[0]

        return __user
