from crum import get_current_user

from core.notificacion.helpers import mass_notify
from custom.authentication.helpers import all_user_with_roles
from .signals import plan_creado, plan_revision_solicitada, plan_aprobado, plan_rechazado, plan_comentado, \
    evaluacion_creada, evaluacion_actualizada
from ...configuracion.signals import configuracion_actualizada


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


plan_creado.connect(notificar_plan_colectivo_creado, dispatch_uid='notificar_plan_colectivo_creado')
plan_revision_solicitada.connect(notificar_solicitud_revision_plan_colectivo,
                                 dispatch_uid='notificar_solicitud_revision_plan_colectivo')
plan_aprobado.connect(notificar_aprobacion_plan_colectivo, dispatch_uid='notificar_aprobacion_plan_colectivo')
plan_rechazado.connect(notificar_rechazo_plan_colectivo, dispatch_uid='notificar_rechazo_plan_colectivo')
plan_comentado.connect(notificar_comentario_plan_colectivo, dispatch_uid='notificar_comentario_plan_colectivo')


def notificar_evaluacion_creada(sender, *args, **kwargs):
    # NOTIFICAR AL POSIBLE GRADUADO
    pass


def notificar_evaluacion_actualizada(sender, *args, **kwargs):
    # NOTIFICAR AL POSIBLE GRADUADO
    pass


evaluacion_creada.connect(notificar_evaluacion_creada, dispatch_uid='notificar_evaluacion_creada')
evaluacion_actualizada.connect(notificar_evaluacion_actualizada, dispatch_uid='notificar_evaluacion_actualizada')


def notificar_configuracion_formacion_colectiva_actualizada(sender, *args, **kwargs):
    if sender.etiqueta in ['etapas_plan_formacion_colectiva', 'comenzar_formacion_colectiva',
                           'planificar_formacion_colectiva']:
        label = sender.etiqueta
        text = None
        if label == 'etapas_plan_formacion_colectiva':
            text = f"La formacion colectiva a cambiado a {sender.valor} etapas"
        elif label == 'comenzar_formacion_colectiva':
            text = f"La planificacion de la formacion colectiva ha {'comenzado' if sender.valor else 'terminado'}"
        elif label == 'planificar_formacion_colectiva':
            text = f"La planificacion de la formacion colectiva en su area ha {'comenzado' if sender.valor else 'terminado'}"

        if text:
            users = all_user_with_roles(['VICERRECTOR', 'JEFE DE AREA', 'DIRECTOR DE RECURSOS HUMANOS'])
            mass_notify(users, get_current_user(), text, {})


configuracion_actualizada.connect(notificar_configuracion_formacion_colectiva_actualizada,
                                  dispatch_uid='notificar_configuracion_formacion_colectiva_actualizada')
