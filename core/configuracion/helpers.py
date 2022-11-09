from core.base.models.modelosSimple import Configuracion


def configValue(key):
    val = None
    try:
        val = Configuracion.objects.get(etiqueta=key).valor
    except Configuracion.DoesNotExist:
        pass
    return val


def isConfigAvailable(key):
    def wrapper(function):
        def can(*args, **kwargs):
            can = configValue(key)
            if can:
                function(*args, **kwargs)

        return can

    return wrapper
