# Create your views here.
from crum import get_current_user
from rest_framework import mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from custom.authentication.models import DirectoryUserAPIKey
from custom.authentication.serializer import CustomAuthTokenSerializer, DirectoryUserSerializer, \
    DirectoryUserAPIKeySerializer


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(True):
            user = serializer.validated_data['user']
            Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)
            user = DirectoryUserSerializer(user).data
            return Response({'token': token.key,'user':user})
        return Response(serializer.errors,HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self,request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response({'detail':'Sesion Cerrada Correctamente'},HTTP_200_OK)



class DirectoryUserAPIKeyView(mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              viewsets.GenericViewSet):

    serializer_class = DirectoryUserAPIKeySerializer
    def get_queryset(self):
        return DirectoryUserAPIKey.objects.filter(user=get_current_user())

    def destroy(self, request, *args, **kwargs):
        super().destroy(request,*args,**kwargs)
        return Response({'detail':'OK'},HTTP_200_OK)