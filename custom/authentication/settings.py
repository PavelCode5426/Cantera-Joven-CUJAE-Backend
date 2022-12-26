from django.conf import settings

SIGENU_URL = getattr(settings, 'SIGENU_URL', None)
SIGENU_USERNAME = getattr(settings, 'SIGENU_USERNAME', None)
SIGENU_PASSWORD = getattr(settings, 'SIGENU_PASSWORD', None)


SIGENU2_URL = getattr(settings, 'SIGENU2_URL', None)
SIGENU2_USERNAME = getattr(settings, 'SIGENU2_USERNAME', None)
SIGENU2_PASSWORD = getattr(settings, 'SIGENU2_PASSWORD', None)
