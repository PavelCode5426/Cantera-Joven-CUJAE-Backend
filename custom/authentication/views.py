# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from custom.authentication.serializer import CustomAuthTokenSerializer, DirectoryUserSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(True):
            user = serializer.validated_data['user']
            Token.objects.filter(user).delete()
            token, created = Token.objects.get_or_create(user=user)
            user = DirectoryUserSerializer(user).data
            return Response({'token': token.key,'user':user})
        return Response(serializer.errors,HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self,request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response({'detail':'Sesion Cerrada Correctamente'},HTTP_200_OK)