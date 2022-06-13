"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view


from helpers import AutoImporter
api_routers_v1 = AutoImporter().loadUrls(['config.urls','custom.administrator.urls'])

api_routers = [
    #Cargando las Versiones de APIS
    path('api/v1/',include(api_routers_v1))
]

swaggerSchema = get_swagger_view(title='Cantera Joven CUJAE',patterns=api_routers)
urlpatterns = api_routers + [
    # Configurando Admin
    path('', include('custom.administrator.urls')),

    # Configurando Swagger Open API
    path('', swaggerSchema, name='doc_swagger'),
]

