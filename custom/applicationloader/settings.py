from django.conf import settings

APPLICATION_LOADER = getattr(settings, 'APPLICATION_LOADER', {
    'EXCLUDE_APPS': [],
    'EXCLUDE_URLS': [],
    'EXCLUDE_ADMIN_MODELS': []
})
