from django.urls import path
from .views import ListUserLogEntries

app_name = 'CustomLogging'

urlpatterns = [
    path('usuario/logs',ListUserLogEntries.as_view())
]
