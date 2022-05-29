from django.contrib import admin
from django.apps import apps

from custom.administrator.form import CustomAdminLoginForm

admin.site.site_title = 'Administrador Cantera Joven CUJAE'
admin.site.index_title = 'Base de Datos Cantera Joven'
admin.site.site_header = 'Administrador Cantera Joven CUJAE'

admin.site.login_form=CustomAdminLoginForm



autoModelsImport = apps.get_models()
for model in autoModelsImport:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered as e:
        pass