# from core.cantera import apps as canteraApps
# from core.familiarizacion import apps as familiarizacionApps
# from core.formacion_complementaria import apps as formacionApps
from helpers import AutoImporter

apps = [
    'core.base.apps.BaseConfig',
    'core.configuracion.apps.ConfiguracionConfig',
]

# apps += canteraApps
# apps += familiarizacionApps
# apps += formacionApps

a = AutoImporter()
a.loadApps()