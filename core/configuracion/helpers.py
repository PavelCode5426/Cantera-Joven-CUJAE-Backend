from core.base.models.modelosSimple import Configuracion
from core.configuracion.proxy import ConfigurationProxy


def config(key):
    return ConfigurationProxy().get(key)


def create_update_configuration(label: str, value, validation: dict = None):
    return Configuracion.objects.update_or_create(etiqueta=label, defaults={
        'etiqueta': label,
        'validacion': validation,
        'valor': value
    })[0]


def isConfigAvailable(key):
    def wrapper(function):
        def can(*args, **kwargs):
            can = config(key)
            if can:
                function(*args, **kwargs)

        return can

    return wrapper
