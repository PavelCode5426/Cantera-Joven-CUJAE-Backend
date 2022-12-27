import requests
from requests.auth import HTTPBasicAuth

from custom.authentication import settings


class SearchOption(object):
    def __init__(self, identification="", name="", lastname="", surname="", email=""):
        self.identification = identification
        self.name = name
        self.lastname = lastname
        self.surname = surname
        self.email = email


class SIGENU_LDAP_Services(object):
    def __init__(self):
        self.base_url = settings.SIGENU_LDAP_URL
        self.username = settings.SIGENU_LDAP_USERNAME
        self.password = settings.SIGENU_LDAP_PASSWORD

    def __request(self, url, method, query_params=None, data=None):
        auth = HTTPBasicAuth(self.username, self.password)
        return requests.request(
            method=method,
            url=f'{self.base_url}/{url}',
            auth=auth,
            params=query_params,
            json=data,
            verify=False
        )

    def login(self, username: str, password: str):
        return self.__request('full-login', 'POST', data=dict(username=username, password=password))

    def search_workers(self, option: SearchOption = SearchOption()):
        return self.__request('search', 'POST', data=option.__dict__)

    def search_persons(self, option: SearchOption = SearchOption()):
        return self.__request('search-all', 'POST', data=option.__dict__)

    def areas(self):
        return self.__request('areas', 'GET').json()

    def workers_by_area(self, distinguishedName: str):
        return self.__request('workers', 'GET', query_params=dict(area=distinguishedName)).json()

    def persons_by_area(self, distinguishedName: str):
        return self.__request('persons', 'GET', query_params=dict(area=distinguishedName)).json()

    def all_persons(self):
        areas = self.areas()
        persons = list()
        count = 1
        for area in areas:
            people = self.persons_by_area(area['distinguishedName'])
            count += 1
            persons += people
        return persons

    def all_workers(self):
        areas = self.areas()
        persons = list()
        count = 1
        for area in areas:
            people = self.workers_by_area(area['distinguishedName'])
            count += 1
            persons += people
        return persons


class SIGENU_Services(object):
    def __init__(self):
        self.base_url = settings.SIGENU_REST_URL
        self.username = settings.SIGENU_REST_USERNAME
        self.password = settings.SIGENU_REST_PASSWORD

    def __request(self, url, method, query_params=None, data=None):
        auth = HTTPBasicAuth(self.username, self.password)
        return requests.request(
            method=method,
            url=f'{self.base_url}/{url}',
            auth=auth,
            params=query_params,
            json=data,
            verify=False
        )

    def students_data(self, carnet: str):
        return self.__request('students', 'GET', data=dict(identification=carnet)).json()

    def carreras(self):
        return self.__request('carreras', 'GET').json()

