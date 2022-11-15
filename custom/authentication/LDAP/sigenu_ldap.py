import json
import random

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


class SIGENU_LDAP(object):
    def __init__(self):
        self.base_url = settings.SIGENU_URL
        self.username = settings.SIGENU_USERNAME
        self.password = settings.SIGENU_PASSWORD

    def __request(self, url, method, query_params=None, data=None):
        auth = HTTPBasicAuth(self.username, self.password)
        return requests.request(
            method=method,
            url=f'{self.base_url}/{url}',
            auth=auth,
            params=query_params,
            json=data
        )

    def login(self, username: str, password: str):
        return self.__request('login', 'POST', data=dict(username=username, password=password))

    def search_workers(self, option: SearchOption = SearchOption()):
        return self.__request('search', 'POST', data=option.__dict__)

    def search_all(self, option: SearchOption = SearchOption()):
        return self.__request('search-all', 'POST', data=option.__dict__)

    def areas(self):
        return self.__request('areas', 'GET')

    def workers_by_area(self, distinguishedName: str):
        return self.__request('workers', 'GET', query_params=dict(area=distinguishedName))

    def persons_by_area(self, distinguishedName: str):
        return self.__request('persons', 'GET', query_params=dict(area=distinguishedName))

    def persons(self):
        areas = self.areas().json()[6:7]
        persons = list()
        count = 1
        for area in areas:
            people = self.persons_by_area(area['distinguishedName']).json()
            print(count)
            count += 1
            persons += people
        return persons

    def persons_titles(self):
        persons = self.persons()
        titles = set()

        for person in persons:
            title = person.get('title', None)
            if title:
                titles.add(title)

        return titles

    def all_persons_types(self):
        persons = self.persons()

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
