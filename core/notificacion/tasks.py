from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string

from config.settings import DEFAULT_FROM_EMAIL
from core.configuracion.helpers import isConfigAvailable
from custom.authentication.models import DirectoryUser
from custom.logging import logger


@isConfigAvailable('enviar_notificaciones_por_correo')
def enviar_notificaciones_por_correo():
    mails = list()
    usuarios = DirectoryUser.objects.distinct().filter(notifications__unread=True).all()

    connection = get_connection()
    connection.open()

    for usuario in usuarios:
        notificaciones = usuario.notifications.unread()
        cantidad = notificaciones.count()

        context = {
            'notificaciones': notificaciones,
            'cantidad': cantidad
        }
        text_content = render_to_string('mail/notification_email_template.txt', context)
        html_content = render_to_string('mail/notification_email_template.html', context)

        mail = EmailMultiAlternatives('Notificaciones Cantera Joven',
                                      body=text_content,
                                      from_email=DEFAULT_FROM_EMAIL,
                                      to=[usuario.email],
                                      connection=connection)
        mail.attach_alternative(html_content, "text/html")
        mails.append(mail)

    connection.send_messages(mails)
    connection.close()
    logger.info('Correos con estado de notificaciones enviados correctamente')
