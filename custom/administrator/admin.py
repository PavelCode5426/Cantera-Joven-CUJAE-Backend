from django.contrib import admin

from custom.administrator.form import CustomAdminLoginForm

admin.site.site_title = 'Administrador Cantera Joven CUJAE'
admin.site.index_title = 'Base de Datos Cantera Joven'
admin.site.site_header = 'Administrador Cantera Joven CUJAE'

admin.site.login_form=CustomAdminLoginForm