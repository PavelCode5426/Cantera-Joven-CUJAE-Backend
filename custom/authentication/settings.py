from django.conf import settings

SIGENU_URL = getattr(settings, 'SIGENU_URL', None)
SIGENU_USERNAME = getattr(settings, 'SIGENU_USERNAME', None)
SIGENU_PASSWORD = getattr(settings, 'SIGENU_PASSWORD', None)
