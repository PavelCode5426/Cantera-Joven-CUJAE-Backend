from crum import get_current_user

from core.notificacion.helpers import mass_notify
from custom.authentication.helpers import all_user_with_roles
from .signals import plan_creado, plan_revision_solicitada, plan_aprobado, plan_rechazado, plan_comentado, \
    evaluacion_creada, evaluacion_actualizada


def notificar_plan_colectivo_creado(sender, *args, **kwargs):
    users = all_user_with_roles(['JEFE DE AREA', 'VICERRECTOR']).all()
    text = "Se ha creado un nuevo plan de formacion colectivo"
    current_user = get_current_user()

    mass_notify(users, current_user, text, {})


def notificar_solicitud_revision_plan_colectivo(sender, *args, **kwargs):
    users = all_user_with_roles(['VICERRECTOR']).all()
    text = "Se ha solicitado revision del plan de formacion colectivo"
    current_user = get_current_user()

    mass_notify(users, current_user, text, {})


def notificar_aprobacion_plan_colectivo(sender, *args, **kwargs):
    users = all_user_with_roles(['DIRECTOR DE RECURSOS HUMANOS']).all()
    text = "Se ha aprobado el plan de formacion colectivo"
    current_user = get_current_user()

    mass_notify(users, current_user, text, {})


def notificar_rechazo_plan_colectivo(sender, *args, **kwargs):
    users = all_user_with_roles(['DIRECTOR DE RECURSOS HUMANOS']).all()
    text = "Se ha rechazado el plan de formacion colectivo"
    current_user = get_current_user()

    mass_notify(users, current_user, text, {})


def notificar_comentario_plan_colectivo(sender, *args, **kwargs):
    text = "Se ha comentado el plan de formacion colectivo"
    current_user = get_current_user()
    users = all_user_with_roles(['DIRECTOR DE RECURSOS HUMANOS', 'VICERECTOR']).exclude(pk=current_user.pk).all()

    mass_notify(users, current_user, text, {})


plan_creado.connect(notificar_plan_colectivo_creado)
plan_revision_solicitada.connect(notificar_solicitud_revision_plan_colectivo)
plan_aprobado.connect(notificar_aprobacion_plan_colectivo)
plan_rechazado.connect(notificar_rechazo_plan_colectivo)
plan_comentado.connect(notificar_comentario_plan_colectivo)


def notificar_evaluacion_creada(sender, *args, **kwargs):
    # NOTIFICAR AL POSIBLE GRADUADO
    pass


def notificar_evaluacion_actualizada(sender, *args, **kwargs):
    # NOTIFICAR AL POSIBLE GRADUADO
    pass


evaluacion_creada.connect(notificar_evaluacion_creada)
evaluacion_actualizada.connect(notificar_evaluacion_actualizada)
