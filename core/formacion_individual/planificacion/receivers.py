from crum import get_current_user
from django.db.models import Max
from notifications.signals import notify

from custom.authentication.helpers import all_user_with_roles
from .helpers import PlanFormacionIndividualHelpers
from .signals import plan_creado, plan_aprobado, plan_rechazado, plan_comentado, plan_revision_solicitada, \
    evaluacion_creada, evaluacion_aprobada, evaluacion_actualizada, actividad_comentada, actividad_revisada, \
    actividad_revision_solicitada
from ...base.models.modelosPlanificacionIndividual import PlanFormacion, EvaluacionFormacion, EtapaFormacion, \
    EvaluacionFinal, ActividadFormacion
from ...base.models.modelosSimple import PropuestaMovimiento
from ...configuracion.helpers import config
from ...configuracion.signals import configuracion_actualizada
from ...notificacion.helpers import mass_notify

"""
*****************************
EVENTOS DEL PLAN DE FORMACION
*****************************
"""


def notificar_aprobacion_del_plan(sender, **kwargs):
    helper = PlanFormacionIndividualHelpers(sender)
    joven = sender.joven
    involucrados = helper.obtener_involucrados()
    current_user = get_current_user()

    description = f"Plan de Formacion Individual del joven {joven.get_full_name()} aprobado"
    for usuario in involucrados:
        notify.send(current_user, recipient=usuario, verb=description, data={})


def notificar_creacion_del_plan(sender, **kwargs):
    helper = PlanFormacionIndividualHelpers(sender)
    joven = sender.joven
    involucrados = helper.obtener_involucrados()
    current_user = get_current_user()

    description = f"Nuevo Plan de Formacion Individual creado para el joven {joven.get_full_name()}"
    for usuario in involucrados:
        notify.send(current_user, recipient=usuario, verb=description, data={})


def notificar_rechazo_del_plan(sender, **kwargs):
    helper = PlanFormacionIndividualHelpers(sender)
    joven = sender.joven
    involucrados = helper.obtener_supervisores()
    current_user = get_current_user()

    description = f"Plan de Formacion Individual del joven {joven.get_full_name()} rechazado"
    for usuario in involucrados:
        notify.send(current_user, recipient=usuario, verb=description, data={})


def notificar_comentario_del_plan(sender, **kwargs):
    helper = PlanFormacionIndividualHelpers(sender)
    joven = sender.joven
    current_user = get_current_user()
    involucrados = list(filter(lambda x: x is not current_user, helper.obtener_involucrados()))

    description = f"Plan de Formacion Individual del joven {joven.get_full_name()} ha sido comentado"
    for usuario in involucrados:
        notify.send(current_user, recipient=usuario, verb=description, data={})


def notificar_solicitud_de_revision_del_plan(sender, **kwargs):
    helper = PlanFormacionIndividualHelpers(sender)
    joven = sender.joven
    current_user = get_current_user()
    involucrados = helper.obtener_supervisores()

    description = f"{current_user.get_full_name()} ha solicitado revision del Plan de Formacion Individual del joven {joven.get_full_name()}"
    for usuario in involucrados:
        notify.send(current_user, recipient=usuario, verb=description, data={})


plan_creado.connect(notificar_creacion_del_plan, dispatch_uid='notificar_creacion_del_plan')
plan_aprobado.connect(notificar_aprobacion_del_plan, dispatch_uid='notificar_aprobacion_del_plan')
plan_rechazado.connect(notificar_rechazo_del_plan, dispatch_uid='notificar_rechazo_del_plan')
plan_comentado.connect(notificar_comentario_del_plan, dispatch_uid='notificar_comentario_del_plan')
plan_revision_solicitada.connect(notificar_solicitud_de_revision_del_plan,
                                 dispatch_uid='notificar_solicitud_de_revision_del_plan')

"""
***************************
EVENTOS DE LAS EVALUACIONES
***************************
"""


def notificar_creacion_de_la_evaluacion(sender, plan=None, etapa=None, **kwargs):
    if etapa:
        plan = PlanFormacion.objects.get(pk=etapa.plan_id)
    helper = PlanFormacionIndividualHelpers(plan)
    current_user = get_current_user()
    supervisores = helper.obtener_supervisores()
    joven = plan.joven

    description = f"{current_user.get_full_name()} ha evaluado el Plan de Formacion Individual del joven {joven.get_full_name()}"
    for usuario in supervisores:
        notify.send(current_user, recipient=usuario, verb=description, data={})

    description = f"{current_user.get_full_name()} ha evaluado el Plan de Formacion Individual"
    notify.send(current_user, recipient=joven, verb=description, data={})


def notificar_actualizacion_de_la_evaluacion(sender, plan=None, etapa=None, **kwargs):
    if etapa:
        plan = PlanFormacion.objects.get(pk=etapa.plan_id)
    helper = PlanFormacionIndividualHelpers(plan)
    current_user = get_current_user()
    supervisores = helper.obtener_supervisores()
    joven = plan.joven

    description = f"{current_user.get_full_name()} ha actualizado la evaluacion del Plan de Formacion Individual del joven {joven.get_full_name()}"
    for usuario in supervisores:
        notify.send(current_user, recipient=usuario, verb=description, data={})

    description = f"{current_user.get_full_name()} ha actualizado la evaluacion del Plan de Formacion Individual"
    notify.send(current_user, recipient=joven, verb=description, data={})


def notificar_aprobacion_de_la_evaluacion(sender, plan=None, **kwargs):
    helper = PlanFormacionIndividualHelpers(plan)
    current_user = get_current_user()
    supervisores = helper.obtener_supervisores()
    joven = plan.joven

    description = f"{current_user.get_full_name()} ha aprobado la evaluacion del Plan de Formacion Individual del joven {joven.get_full_name()}"
    for usuario in supervisores:
        notify.send(current_user, recipient=usuario, verb=description, data={})

    description = f"{current_user.get_full_name()} ha aprobado la evaluacion del Plan de Formacion Individual"
    notify.send(current_user, recipient=joven, verb=description, data={})


def gestionar_la_aprobacion_de_la_evaluacion(sender, plan: PlanFormacion = None, **kwargs):
    if isinstance(sender, EvaluacionFinal):
        propuesta = PropuestaMovimiento.objects.get(nombre='Prorroga')
        if propuesta == sender.propuestaMovimiento:
            config_key = 'etapas_de_prorroga_formacion_individual'
            plan = sender.planformacion
            numero_max = EtapaFormacion.objects.filter(plan_id=plan.pk).aggregate(Max('numero'))['numero__max']

            for i in range(numero_max + 1, numero_max + config(config_key)):
                EtapaFormacion.objects.create(plan_id=plan.pk, esProrroga=True, numero=i)

            plan.estado = plan.Estados.ENDESARROLLO
            plan.aprobadoPor = None
            plan.save()
        else:
            plan.estado = plan.Estados.FINALIZADO
            plan.save()

    elif isinstance(sender, EvaluacionFormacion):
        if sender.cerrarPlan:
            etapas = EtapaFormacion.objects.filter(plan_id=plan.pk, evaluacion=None).all()
            for etapa in etapas:
                etapa.evaluacion = EvaluacionFormacion.objects.create(texto="Etapa satisfactoria cerrada por defecto",
                                                                      aprobadoPor=get_current_user())
                etapa.save()

        elif sender.replanificar:
            plan.estado = plan.Estados.ENDESARROLLO
            plan.save()


evaluacion_creada.connect(notificar_creacion_de_la_evaluacion, dispatch_uid='notificar_creacion_de_la_evaluacion')
evaluacion_actualizada.connect(notificar_actualizacion_de_la_evaluacion,
                               dispatch_uid='notificar_actualizacion_de_la_evaluacion')
evaluacion_aprobada.connect(notificar_aprobacion_de_la_evaluacion, dispatch_uid='notificar_aprobacion_de_la_evaluacion')
evaluacion_aprobada.connect(gestionar_la_aprobacion_de_la_evaluacion,
                            dispatch_uid='gestionar_la_aprobacion_de_la_evaluacion')

"""
***************************
EVENTOS DE LAS ACTIVIDADES
***************************
"""


def notificar_revision_de_la_actividad(sender, plan: PlanFormacion, **kwargs):
    actividad = sender
    helper = PlanFormacionIndividualHelpers(plan)
    joven = plan.joven
    current_user = get_current_user()
    involucrados = list(filter(lambda x: x is not current_user, helper.obtener_tutores()))
    involucrados.append(joven)

    description = f"En el Plan de Formacion Individual del joven {joven.get_full_name()} la actividad {actividad.nombre} ha sido marcada como revisada"
    for usuario in involucrados:
        notify.send(current_user, recipient=usuario, verb=description, data={})


def notificar_comentario_de_la_actividad(sender, plan: PlanFormacion, actividad: ActividadFormacion, **kwargs):
    helper = PlanFormacionIndividualHelpers(plan)
    joven = plan.joven
    current_user = get_current_user()
    involucrados = list(filter(lambda x: x is not current_user, helper.obtener_tutores()))
    involucrados.append(joven)

    description = f"Plan de Formacion Individual del joven {joven.get_full_name()} ha sido comentado en la actividad {actividad.nombre}"
    for usuario in involucrados:
        notify.send(current_user, recipient=usuario, verb=description, data={})


def notificar_solicitud_de_revison_de_la_actividad(sender, plan: PlanFormacion, **kwargs):
    actividad = sender
    helper = PlanFormacionIndividualHelpers(plan)
    joven = plan.joven
    current_user = get_current_user()
    involucrados = list(filter(lambda x: x is not current_user, helper.obtener_tutores()))

    description = f"El joven {joven.get_full_name()} ha solicitado revison de la actividad {actividad.nombre}"
    for usuario in involucrados:
        notify.send(current_user, recipient=usuario, verb=description, data={})


actividad_revision_solicitada.connect(notificar_solicitud_de_revison_de_la_actividad,
                                      dispatch_uid='notificar_cumplimiento_de_la_actividad')
actividad_revisada.connect(notificar_revision_de_la_actividad, dispatch_uid='notificar_revison_de_la_actividad')
actividad_comentada.connect(notificar_comentario_de_la_actividad, dispatch_uid='notificar_comentario_de_la_actividad')

"""
*****************************************
EVENTOS DE ACTUALIZACION DE CONFIGURACION
*****************************************
"""


def notificar_configuracion_formacion_individual_actualizada(sender, *args, **kwargs):
    if sender.etiqueta in ['etapas_plan_formacion_individual_graduado', 'etapas_plan_formacion_individual_estudiante',
                           'etapas_de_prorroga_formacion_individual', 'comenzar_formacion_individual']:
        label = sender.etiqueta
        text = None
        if label == 'etapas_plan_formacion_individual_graduado':
            text = f"Las cantidad de etapas de la formacion individual del recien graduado ha cambiado a {sender.valor} por plan"
        elif label == 'etapas_plan_formacion_individual_estudiante':
            text = f"Las cantidad de etapas de la formacion individual del estudiante ha cambiado a {sender.valor} por plan"
        elif label == 'etapas_de_prorroga_formacion_individual':
            text = f"Las cantidad de etapas de la formacion individual a cambiado a {sender.valor} por prorroga"
            text = f"La planificacion de la formacion colectiva en su area ha {'comenzado' if sender.valor else 'terminado'}"
        elif label == 'comenzar_formacion_individual':
            text = f"La planificacion de la formacion individual en su area ha {'comenzado' if sender.valor else 'terminado'}"

        if text:
            users = all_user_with_roles(['VICERRECTOR', 'JEFE DE AREA', 'DIRECTOR DE RECURSOS HUMANOS', 'TUTOR'])
            mass_notify(users, get_current_user(), text, {})


configuracion_actualizada.connect(notificar_configuracion_formacion_individual_actualizada,
                                  dispatch_uid='notificar_configuracion_formacion_individual_actualizada')
