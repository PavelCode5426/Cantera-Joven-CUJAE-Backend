from django.apps import AppConfig


class ApplicationLoaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom.applicationloader'
    verbose_name = 'Application Dinamic Loader'
    label = 'application_loader'

    _urls: list
    __apps: list
    __admin_models: list

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self._urls = list()
        self.__apps = list()
        self.__admin_models = list()

    # def ready(self):
    #     from custom.applicationloader.helper import AppsLoader, UrlsLoader, AdminLoader
    #     from .settings import APPLICATION_LOADER
    #
    #     apps_loader = AppsLoader(APPLICATION_LOADER['EXCLUDE_APPS'])
    #     apps_loader.load()
    #     self.__apps = apps_loader.get_apps()
    #
    #     urls_loader = UrlsLoader(APPLICATION_LOADER['EXCLUDE_URLS'])
    #     urls_loader.load()
    #     self._urls = urls_loader.get_urls()
    #
    #     admin_loader = AdminLoader(APPLICATION_LOADER['EXCLUDE_ADMIN_MODELS'])
    #     admin_loader.load()
    #     self.__admin_models = admin_loader.get_models()

    def get_urls(self):
        return self._urls

    def get_apps(self):
        return self.__apps

    def get_admin_models(self):
        return self.__admin_models
