from django.test import TestCase

# Create your tests here.
from core.notificacion.notifications import TelegramNotification
from .tasks import enviar_estado_notificaciones_por_correo


class TestNotifications(TestCase):
    def test_sendNotification(self):
        telegram = TelegramNotification()
        telegram.send()

    def test_send_email(self):
        enviar_estado_notificaciones_por_correo()
