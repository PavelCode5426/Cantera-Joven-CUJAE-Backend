from crum import get_current_user

from core.notificacion.helpers import mass_notify
from custom.authentication.helpers import all_user_with_roles
from .signals import preubicacion_creada
from ...configuracion.signals import configuracion_actualizada


def notificar_creacion_preubicacion_laboral(sender, *args, **kwargs):
    text = "Se ha realizado la preubicación laboral de posibles graduados a áreas"
    current_user = get_current_user()
    users = all_user_with_roles(['DIRECTOR DE RECURSOS HUMANOS']).exclude(pk=current_user.pk).all()

    mass_notify(users, current_user, text, {})

preubicacion_creada.connect(notificar_creacion_preubicacion_laboral, dispatch_uid='notificar_creacion_preubicacion_laboral')


