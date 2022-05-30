from django.urls import path
from rest_framework import routers

from .views import ListarObtenerArea

# Create your views here.
app_name = 'GestionarArea'

router = routers.SimpleRouter()
router.register('area',ListarObtenerArea,'Area')

urlpatterns = router.urls + []