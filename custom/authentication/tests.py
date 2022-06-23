from django.test import TestCase
# Create your tests here.
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

AUTH_LOGIN_URL=reverse('Authentication:login')
AUTH_LOGOUT_URL=reverse('Authentication:logout')


class AuthenticationTestCase(TestCase):
    def login(self,user,passw):
        return self.client.post(AUTH_LOGIN_URL,{'username':user,'password':passw})

    def setUp(self) -> None:
        self.client = APIClient()
    def test_login_user_test(self):
        login_result = self.login('pperez','1234').data

        self.assertTrue(login_result.get('token'))
        self.assertTrue(login_result.get('user').get('username')== 'pperez')

        login_result = self.login('pperez','1234').data

        self.assertIsNone(login_result.get('token'))
        self.assertIsNone(login_result.get('user'))
        self.assertEqual(login_result.get('detail')[0].title(),'No Puede Iniciar Sesión Con Las Credenciales Proporcionadas.')

    def test_logout_user(self):
        logout_result = self.client.post(AUTH_LOGOUT_URL).data

        self.assertTrue(logout_result.get('detail'))
        self.assertEqual(logout_result.get('detail'),'Las credenciales de autenticación no se proveyeron.')

        token = self.login('pperez','1234').data.get('token')
        self.client.head({'Token':token})
        logout_result = self.client.post(AUTH_LOGOUT_URL)


        logout_result = self.client.post(AUTH_LOGOUT_URL)

    def test_autoupdate_user(self):
        from .tasks import actualizar_informacion_usuarios
        actualizar_informacion_usuarios()


