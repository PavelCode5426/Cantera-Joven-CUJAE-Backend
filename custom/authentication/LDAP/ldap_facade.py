import json
import random

import openpyxl
from django.conf import settings

from core.base.models.modelosSimple import Area
from custom.authentication.LDAP.sigenu_ldap_services import SIGENU_LDAP_Services, SearchOption
from custom.authentication.models import DirectoryUser

GRADUATE_TEACHING_CATEGORIES = [
    'INSTRUCTOR RECIÉN GRADUADO',
    'RECIÉN GRADUADO EN ADIESTRAMIENTO (TM)',
    'RECIÉN GRADUADO EN ADIESTRAMIENTO (NS)'
]


def is_student(value):
    _is = False
    if 'personType' in value:
        _is = value['personType'] == 'Student'

    return _is


def is_graduate(value):
    _is = False
    if 'teachingCategory' in value:
        teachingCategory = str(value['teachingCategory'])
        _is = 'RECIÉN GRADUADO' in teachingCategory.lower() or teachingCategory in GRADUATE_TEACHING_CATEGORIES

    return _is


def is_supergraduate(value):
    return is_graduate(value) and not str(value['teachingCategory']).count('(TM)')


def is_pgraduate(value):
    _is = False
    if 'personExternal' in value:
        _is = value['personExternal'] == 'TRUE'

    return _is


def is_tutor(value):
    _is = not bool(is_graduate(value) or is_pgraduate(value) or is_student(value))
    return _is


def get_cuadro_excel_info(value):
    info = None
    workbook = openpyxl.load_workbook(settings.MEDIA_ROOT + '/excels/cuadros.xlsx', read_only=True)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2):
        if str(row[3].value) == value['identification']:
            # info = [cell.value for cell in row]
            info = dict(
                JArea=bool(row[4].value),
                DRHumanos=bool(row[5].value),
                VRPrimero=bool(row[6].value),
            )
            break

    workbook.close()
    return info


def is_cuadro(value):
    return bool(get_cuadro_excel_info(value))


class LDAPFacade:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LDAPFacade, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.sigenu_ldap_service = SIGENU_LDAP_Services()

    def authentication(self, username, password):
        user = None
        response = self.sigenu_ldap_service.login(username, password)

        if response.status_code == 200:
            user = response.json()
            user = self.__parse_authentication_response(user)

        return user

    def __parse_authentication_response(self, response):
        response = response['user']
        parse_response = dict(
            address=response['streetAddress'],
            email=response['mail'],
            identification=response['cUJAEPersonDNI'],
            personType=response['cUJAEPersonType'],
            phone=response['telephoneNumber'],
            user=response['sAMAccountName'],
            personExternal=response['cUJAEPersonExternal'],
            areaId=response['distinguishedName'],
            name=response['givenName'],
            lastname=response['sn']
        )

        if 'department' in response:
            parse_response['department'] = response['department']
        if 'title' in response:
            parse_response['teachingCategory'] = response['title']
        if 'o' in response:
            parse_response['area'] = response['o']

        if parse_response['personType'] == 'Student':
            parse_response['studentCourse'] = response['cUJAEStudentCourse']
            parse_response['studentYear'] = response['cUJAEStudentYear']
            parse_response['studentGroup'] = response['cUJAEStudentGroup']
            parse_response['studentTemporal'] = response['cUJAEStudentTemporal']

        return parse_response

    def all_persons_from_area(self, distinguishedName: str):
        return self.sigenu_ldap_service.persons_by_area(distinguishedName)

    def all_students_from_area(self, distinguishedName: str):
        persons = self.all_persons_from_area(distinguishedName)
        persons = list(filter(is_student, persons))
        return persons

    def all_pgraduates(self):
        persons = self.sigenu_ldap_service.all_persons()
        persons = list(filter(is_pgraduate, persons))
        return persons

    def all_graduates_from_area(self, distinguishedName: str):
        persons = self.sigenu_ldap_service.workers_by_area(distinguishedName)
        persons = list(filter(is_graduate, persons))
        return persons

    def all_graduates(self):
        persons = self.sigenu_ldap_service.all_persons()
        persons = list(filter(is_graduate, persons))
        return persons

    def all_tutors_from_area(self, distinguishedName: str):

        persons = self.sigenu_ldap_service.workers_by_area(distinguishedName)
        persons = list(filter(is_tutor, persons))
        return persons

    def all_persons_with_filter(self, search: SearchOption = None):

        if search:
            persons = self.sigenu_ldap_service.search_persons(search)
        else:
            persons = self.sigenu_ldap_service.all_persons()

        return persons

    def all_workers_with_filter(self, search: SearchOption = None):

        if search:
            persons = self.sigenu_ldap_service.search_workers(search)
        else:
            persons = self.sigenu_ldap_service.all_workers()

        return persons

    def all_students_with_filter(self, search: SearchOption = None):
        persons = self.all_persons_with_filter(search)
        persons = list(filter(is_student, persons))
        return persons

    def all_pgraduates_with_filter(self, search: SearchOption = None):
        persons = self.all_persons_with_filter(search)
        persons = list(filter(is_pgraduate, persons))
        return persons

    def all_graduates_with_filter(self, search: SearchOption = None):
        persons = self.all_workers_with_filter(search)
        persons = list(filter(is_graduate, persons))
        return persons

    def all_areas(self):
        return self.sigenu_ldap_service.areas()

    # IMPLEMENTADO PARA PROBAR, BORRAR
    def all_areas_with_departments(self):
        areas = self.all_areas()
        elements = []

        for area in areas:
            subareas = set()

            persons = self.all_persons_from_area(area['distinguishedName'])

            for person in persons:
                if 'department' in person:
                    subareas.add(person['department'])

            elements.append({
                'area': area,
                'subareas': list(subareas)
            })

        return elements

    def get_person_roles(self, person_ldap_data: dict) -> list:
        roles = list()

        if is_graduate(person_ldap_data):
            roles.append('RECIEN GRADUADO')
        elif is_pgraduate(person_ldap_data):
            roles.append('POSIBLE GRADUADO')
        elif is_student(person_ldap_data):
            roles.append('ESTUDIANTE')

        if not len(roles):  # COMPRUEBA CUANDO NO ES NINGUN ROL DE JOVEN
            if is_tutor(person_ldap_data):
                roles.append('TUTOR')

            cuadro_data = get_cuadro_excel_info(person_ldap_data)
            if cuadro_data:
                if cuadro_data['JArea']:
                    roles.append('JEFE DE AREA')
                if cuadro_data['DRHumanos']:
                    roles.append('DIRECTOR DE RECURSOS HUMANOS')
                if cuadro_data['VRPrimero']:
                    roles.append('VICERRECTOR')

        return roles

    def update_or_insert_area(self, areaData: dict):
        area = None
        if areaData.get('area', None):
            area_str = areaData['area']
            area = Area.objects.filter(nombre=area_str).first()

            department_str = areaData.get('department', None)
            department = Area.objects.filter(nombre=department_str).first()

            not_area = not area
            not_department = (bool(department_str) and not department)

            if not_area or not_department:
                areas_with_departments = self.all_areas_with_departments()
                areas = []

                for item in areas_with_departments:
                    _area = Area.objects.update_or_create(nombre=item['name'], defaults={**item})[0]
                    areas.append(_area)
                    for depart in item['subareas']:
                        _area = Area.objects.update_or_create(nombre=depart, defaults={"nombre": depart})[0]
                        areas.append(_area)

                if not_department:
                    area = next(filter(lambda x: x.nombre == department_str, areas))
                else:
                    area = next(filter(lambda x: x.nombre == area_str, areas))

        return area

    def update_or_insert_user(self, user_data: dict):
        data = dict(
            first_name=user_data['name'],
            last_name=user_data['lastname'],
            direccion=user_data['address'],
            cargo=None if 'teachingCategory' not in user_data else user_data['teachingCategory'],
            carnet=user_data['identification'],
            directorioID=user_data['areaId'],
            telefono=user_data['phone'],
            email=user_data['email'],
            username=user_data['user'],
            area=self.update_or_insert_area({
                'area': user_data.get('area', None),
                'department': user_data.get('department', None)
            })
        )

        user, created = DirectoryUser.objects.update_or_create(directorioID=data['directorioID'], defaults=data)

        # if is_student(userData):
        #     data['anno_academico'] = userData['studentYear']
        #     Estudiante(user)
        # elif is_graduate(userData):
        #     data['esNivelSuperior'] = '(NS)' in data['cargo']
        #     data['esExterno'] = userData['personExternal']

        # elif is_pgraduate(userData):#NO LO ACTUALIZO PORQUE NO TIENE NADA
        #     model = PosibleGraduado

        return user

    # METODOS PRIVADOS
    # IMPLEMENTADO PARA PROBAR, BORRAR
    def __all_persons_types(self):
        persons = self.sigenu_ldap_service.all_persons()

        random.shuffle(persons)

        clear_list = list()
        while len(persons) > 0:
            person = persons[0]

            clear_list.append(person)

            def filter_function(value):
                value_keys = list(value.keys())
                person_keys = list(person.keys())
                return len(value_keys) != len(person_keys) or not all(item in person_keys for item in value_keys)

            persons = list(filter(filter_function, persons))

        out_file = open("persons.json", "w")
        json.dump(clear_list, out_file, indent=6, sort_keys=True)
        out_file.close()
        return clear_list

    def __all_teachingCategories(self):
        persons = self.sigenu_ldap_service.all_persons()
        titles = set()

        for person in persons:
            title = person.get('teachingCategory', None)
            if title:
                titles.add(title)

        return titles
