from core.base.models.modelosUsuario import PosibleGraduado
from core.configuracion.helpers import isConfigAvailable
from custom.authentication.LDAP.ldap_facade import LDAPFacade
from custom.logging import logger


@isConfigAvailable('mantener_actualizada_informacion_de_posibles_graduados')
def actualizar_informacion_posibles_graduados():
    directory_users = LDAPFacade().all_pgraduates
    importados = PosibleGraduado.objects.filter(is_active=True).all()
    usuarios_perdidos = list()
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
                    ldap_user = None
            except StopIteration:
                pass

            if not ldap_user:
                text += f'* No se encontro al usuario {current.get_full_name()} con CI {current.carnet}\n'
                current.is_active = False
                usuarios_perdidos.append(current)
            else:
                LDAPFacade().update_or_insert_user(ldap_user)

    except StopIteration as e:
        PosibleGraduado.objects.bulk_update(usuarios_perdidos, ['is_active'])
        if text:
            logger.critical(f'Error importando posibles graduados\n{text}')
