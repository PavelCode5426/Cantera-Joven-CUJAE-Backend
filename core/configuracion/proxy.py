from abc import abstractmethod
from typing import Any

from core.base.patterns import Singleton


# TODO PERFECCIONAR EL PATRON
class VariableNotFoundException(Exception):
    pass


class AbstractConfiguration:

    @abstractmethod
    def get(self, label: str) -> Any:
        pass


class ConfigurationProxy(AbstractConfiguration, Singleton):

    def __init__(self):
        self.load_config()

    def get(self, label: str) -> Any:
        value = getattr(self, label, None)
        if value is None:
            self.load_config()
            value = getattr(self, label, None)
            if value is None:
                raise VariableNotFoundException

        return value

    def load_config(self):
        from core.base.models.modelosSimple import Configuracion
        for config in Configuracion.objects.all():
            setattr(self, config.etiqueta, config.valor)
