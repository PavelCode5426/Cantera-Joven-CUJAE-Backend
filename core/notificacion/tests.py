from django.test import TestCase

# Create your tests here.
from core.notificacion.notifications import TelegramNotification
from .tasks import enviar_estado_notificaciones_por_correo


class TestNotifications(TestCase):

    def test_send_simple_mail(self):

        from django.core.mail import send_mail,settings
        c = send_mail('asunto', 'mensaje', 'from@example.com',['to@example.com'], fail_silently=False)


"""
    def test_send_email(self):
        enviar_estado_notificaciones_por_correo()
"""


