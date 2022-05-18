from django.urls import path, include
from rest_framework import routers

from custom.authentication.views import DirectoryUserAPIKeyView
from .views import CustomObtainAuthToken,LogoutAPIView


#Importante colocar el app_name y el urlpatterns (NO PUEDE SER OTRO NOMBRE)

app_name = 'Authentication'
viewset_patterns = routers.SimpleRouter()
viewset_patterns.register('api-key', DirectoryUserAPIKeyView, 'api-key')

urlpatterns = [
    path('',include(viewset_patterns.urls)),
    path('login',CustomObtainAuthToken.as_view(),name='login'),
    path('logout',LogoutAPIView.as_view(),name='logout'),
]
