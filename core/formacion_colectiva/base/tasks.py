from core.base.models.modelosUsuario import PosibleGraduado
from core.configuracion.helpers import isConfigAvailable
from custom.authentication.LDAP.ldap_facade import LDAPFacade
from custom.authentication.LDAP.sigenu_ldap_services import SIGENU_LDAP_Services
from custom.logging import logger


@isConfigAvailable('mantener_actualizada_informacion_de_posibles_graduados')
def actualizar_informacion_posibles_graduados():
    directory_users = LDAPFacade().all_pgraduates
    importados = PosibleGraduado.objects.filter(is_active=True).all()
    it = iter(importados)
    text = ''

    try:
        while True:
            current = next(it)
            ldap_iterator = iter(directory_users)
            ldap_user = None
            try:
                while True:
                    user = next(ldap_iterator)

                    if user.get('identification') == current.carnet:
                        ldap_user = user
                        directory_users.remove(ldap_user)
                        raise StopIteration
            except StopIteration:
                current.is_active = False

            if not ldap_user:
                text += f'* No se encontro al posible graduado {current.get_fullname()} con CI {current.carnet}\n'
                logger.critical()
            else:
                current.fist_name = ldap_user.get('name')
                #TODO SEGUIN CAMBIANDO COSAS
                #current.save()

    except StopIteration as e:
        PosibleGraduado.objects.bulk_update(importados)
        if text:
            logger.critical(f'Error importando posibles graduados\n{text}')



