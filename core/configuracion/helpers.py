from core.base.models.modelosSimple import Configuracion


def configValue(key):
    val = None
    val = Configuracion.objects.get(etiqueta=key).valor
    return val


def create_update_configuration(label: str, value, validation: dict = None):
    return Configuracion.objects.update_or_create(etiqueta=label, defaults={
        'etiqueta': label,
        'validacion': validation,
        'valor': value
    })[0]


def isConfigAvailable(key):
    def wrapper(function):
        def can(*args, **kwargs):
            can = configValue(key)
            if can:
                function(*args, **kwargs)

        return can

    return wrapper
