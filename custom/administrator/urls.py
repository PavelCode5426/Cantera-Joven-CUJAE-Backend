from django.contrib import admin
from django.urls import path

# Create your views here.
urlpatterns = [
    path('admin/',admin.site.urls)
]