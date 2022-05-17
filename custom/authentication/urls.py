from django.urls import path
from rest_framework import routers

from .views import CustomObtainAuthToken,LogoutAPIView


#Importante colocar el app_name y el urlpatterns (NO PUEDE SER OTRO NOMBRE)

app_name = 'Authentication'
viewset_patterns = routers.SimpleRouter()

urlpatterns = viewset_patterns.urls + [
    path('login',CustomObtainAuthToken.as_view(),name='login'),
    path('logout',LogoutAPIView.as_view(),name='logout')
]
