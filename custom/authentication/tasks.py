from core.configuracion.helpers import isConfigAvailable
from custom.authentication.LDAP.ldap_facade import LDAPFacade
from custom.authentication.models import DirectoryUser
from custom.logging import logger


@isConfigAvailable('mantener_actualizada_informacion_de_usuarios')
def actualizar_informacion_usuarios():
    directory_users = LDAPFacade().all_persons_with_filter()
    importados = DirectoryUser.objects.filter(is_active=True, posiblegraduado=None).all()
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
            except StopIteration:
                pass

            if not ldap_user:
                text += f'* No se encontro al usuario {current.get_full_name()} con CI {current.carnet}\n'
                current.is_active = False
                usuarios_perdidos.append(current)
            else:
                LDAPFacade().update_or_insert_user(ldap_user)


    except StopIteration as e:
        DirectoryUser.objects.bulk_update(usuarios_perdidos, ['is_active'])
        if text:
            logger.critical(f'Error importando usuarios durante la actualizacion automatica\n{text}')
