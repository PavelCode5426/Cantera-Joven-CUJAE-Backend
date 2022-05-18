from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Graduado)
admin.site.register(models.GraduadoTutor)

admin.site.register(models.Solicitud)
admin.site.register(models.SolicitudTutor)