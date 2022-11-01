import glob
import importlib

from django.conf import settings

APPLICATION_LOADER = getattr(settings, 'APPLICATION_LOADER', {
    'EXCLUDE_APPS': [],
    'EXCLUDE_ADMIN_MODELS': []
})


class ApplicationLoader:
    __doc__ = 'Clase responsable de cargar automaticamente la aplicacion' \
              '* Apps.py' \
              '* Urls.py' \
              '* Admins.py'

    def _checkInExclude(self, element, list: list):
        element = element if isinstance(element, str) else '{module}.{name}'.format(module=element.__module__,
                                                                                    name=element.__name__)
        found = False
        it = iter(list)
        try:
            item = next(it)
            while item and not found:
                if str(item).endswith('*'):  # Excluir Path
                    found = element.startswith(item[:-1])
                elif str(item).__contains__('.') and element == item:  # Excluir archivo o clase
                    found = True
                else:  # Excluir elemento
                    found = item.endswith(element)
                item = next(it)
        except StopIteration:
            pass

        return found

    def cleanPath(self, file):
        file = file.replace('\\', '.')
        file = file.replace('.py', '')
        return file

    def loadApps(self, join=[]) -> list:
        exclude = APPLICATION_LOADER['EXCLUDE_APPS']
        self.apps = set()
        prefix = '**/apps.py'
        for file in glob.glob(prefix, recursive=True):
            file = self.cleanPath(file.__str__())
            appsInported = importlib.import_module(file)
            for app in dir(appsInported):
                if not app.startswith('__') and not self._checkInExclude(app, exclude):
                    self.apps.add(file + '.' + app)
        # return list( set(join and self.apps) ) #TODO Arreglar esto
        return self.apps

    def loadUrls(self):
        self.urls = dict()
        exclude = APPLICATION_LOADER['EXCLUDE_APPS']
        prefix = '**/urls.py'
        for file in glob.glob(prefix, recursive=True):
            file = self.cleanPath(file.__str__())
            if not self._checkInExclude(file, exclude):
                appsInported = __import__(file, globals(), locals(), ['app_name', 'app_prefix'], 0)
                app_prefix = appsInported.app_prefix if hasattr(appsInported, 'app_prefix') else ''
                if hasattr(appsInported, 'app_name'):
                    self.urls[appsInported.app_name] = (app_prefix, file)

        returnList = list()
        from django.urls import path, include
        for index in self.urls:
            returnList.append(path(self.urls[index][0], include(self.urls[index][1], namespace=index)))

        return returnList

    def loadModelsInAdmin(self):
        from django.apps import apps
        from django.contrib import admin

        # admin.site._registry.clear()
        exclude = APPLICATION_LOADER['EXCLUDE_ADMIN_MODELS']
        autoModelsImport = apps.get_models()
        for model in autoModelsImport:
            try:
                if not self._checkInExclude(model, exclude):
                    admin.site.register(model)
            except admin.sites.AlreadyRegistered as e:
                pass
                # print("El {m} ya se encuentra registrado ".format(m=model.__name__))
