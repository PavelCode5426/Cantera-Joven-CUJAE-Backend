from django.conf import settings

SIGENU_LDAP_URL = getattr(settings, 'SIGENU_LDAP_URL', None)
SIGENU_LDAP_USERNAME = getattr(settings, 'SIGENU_LDAP_USERNAME', None)
SIGENU_LDAP_PASSWORD = getattr(settings, 'SIGENU_LDAP_PASSWORD', None)

SIGENU_REST_URL = getattr(settings, 'SIGENU_REST_URL', None)
SIGENU_REST_USERNAME = getattr(settings, 'SIGENU_REST_USERNAME', None)
SIGENU_REST_PASSWORD = getattr(settings, 'SIGENU_REST_PASSWORD', None)
PROXIES = getattr(settings, 'PROXIES', None)
