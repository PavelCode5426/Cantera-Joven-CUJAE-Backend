from django.contrib import admin
from django.urls import path
from .views import GestionarConfiguracion

# Create your views here.
app_name = 'SystemConfiguration'

urlpatterns = [
    path('',GestionarConfiguracion.as_view()),
    path('/<int:pk>',GestionarConfiguracion.as_view())
]