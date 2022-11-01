import glob
import importlib


class AbstractApplicationLoader:
    exclude_list: list

    def __init__(self, exclude: list = []):
        self.exclude_list = exclude

    def _checkInExclude(self, element):
        element = element if isinstance(element, str) else '{module}.{name}'.format(module=element.__module__,
                                                                                    name=element.__name__)
        found = False
        it = iter(self.exclude_list)
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

    def load(self):
        raise NotImplementedError()


class AppsLoader(AbstractApplicationLoader):
    apps: set

    def __init__(self, exclude: list = []):
        self.apps = set()
        default_exclude = [
            'AppConfig'  # EXCLUIR ESTA CLASE OBLIGATORIAMENTE
        ]
        super().__init__(exclude + default_exclude)

    def load(self):
        prefix = '**/apps.py'
        for file in glob.iglob(prefix, recursive=True):
            file = self.cleanPath(file.__str__())
            appsInported = importlib.import_module(file).__dict__

            for app in appsInported:
                if not app.startswith('__') and not self._checkInExclude(app):
                    app_module = appsInported[app].__module__
                    app_name = appsInported[app].__name__
                    self.apps.add(f'{app_module}.{app_name}')

    def get_apps(self):
        return self.apps


class UrlsLoader(AbstractApplicationLoader):
    urls: list

    def __init__(self, exclude: list = []):
        self.urls = list()
        default_exclude = [

        ]
        super().__init__(exclude + default_exclude)

    def load(self):
        from django.urls import path, include

        urls = dict()
        prefix = '**/urls.py'
        for file in glob.glob(prefix, recursive=True):
            file = self.cleanPath(file.__str__())
            if not self._checkInExclude(file):
                appsInported = importlib.import_module(file).__dict__

                app_prefix = appsInported['app_prefix'] if 'app_prefix' in appsInported else ''
                if 'app_name' in appsInported:
                    app_name = appsInported['app_name']
                    self.urls.append(path(app_prefix, include(file, namespace=app_name)))

    def get_urls(self):
        return self.urls


class AdminLoader(AbstractApplicationLoader):
    models: set

    def __init__(self, exclude: list = []):
        self.models = set()
        default_exclude = [

        ]
        super().__init__(exclude + default_exclude)

    def load(self):
        from django.apps import apps
        from django.contrib import admin
        # admin.site._registry.clear()
        autoModelsImport = apps.get_models()
        for model in autoModelsImport:
            try:
                if not self._checkInExclude(model):
                    admin.site.register(model)
                    self.models.add(model)
            except admin.sites.AlreadyRegistered as e:
                pass
                # print("El {m} ya se encuentra registrado ".format(m=model.__name__))

    def get_models(self):
        return self.models
