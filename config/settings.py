"""
Django settings for app project.

Generated by 'django-administrator startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os

# INSTALANDO VARIABLES DE ENTORNO
import environ
from django.conf.global_settings import MEDIA_ROOT

from custom.applicationloader.helper import AppsLoader

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'django-insecure-pbfwo%(a1b4uu+1+4mhwm)$m7d64)^v9lx6$mg5qz0!k9pr5y8')
)

# Set the project base directory
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
# Si encuentra el archivo combina las variables de entorno por las del archivo
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: don't run with debug turned on in production!
# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/


ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:3000',
# )


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'annoying',

    # Libs Instaladas
    'rest_framework',
    'rest_framework_swagger',
    'django_seed',
    'django_q',
    'notifications',
    'django_filters',

    # Libs de Autenticacion
    'rest_framework.authtoken',

    # Modulos Ajustados
    'custom.authentication',
    'custom.administrator',
    'custom.logging',

    # Modulos Instalados
    'core.base',
    'core.configuracion',
    'core.notificacion',

    'core.formacion_colectiva.base',
    'core.formacion_colectiva.gestionar_area',
    'core.formacion_colectiva.planificacion',

    'core.formacion_individual.base',
    'core.formacion_individual.gestionar_avales',
    'core.formacion_individual.gestionar_solicitar_tutor',
    'core.formacion_individual.planificacion',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    # Custom Middlewares
    'crum.CurrentRequestUserMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'template'),
            os.path.join(BASE_DIR, 'core/notificacion/template'),
            os.path.join(BASE_DIR, 'core/formacion_individual/planificacion/template'),
            os.path.join(BASE_DIR, 'core/formacion_colectiva/planificacion/template'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'ATOMIC_REQUEST': True
    } if env('DATABASE_HOST', default=None) else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/database/db.sqlite3',
        'ATOMIC_REQUEST': True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.authentication.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.authentication.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.authentication.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.authentication.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-cu'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
MEDIA_ROOT = BASE_DIR + '/media'
MEDIA_URL = 'media/'
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.DirectoryUser'

AUTHENTICATION_BACKENDS = [
    'custom.authentication.backend.DirectorioOnlineAuthBackend',  # Autenticacion en Directorio Online
    'custom.authentication.backend.DirectorioLocalAuthBackend',  # Autenticacion en Directorio Local
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.authentication` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'custom.authentication.backend.APIKeyAuthentication',
        'custom.authentication.backend.BearerAuthentication'
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.base.pagination.StandardResultsSetPagination',
    'DEFAULT_METADATA_CLASS': 'core.base.metadata.MinimalMetadata',
    'EXCEPTION_HANDLER': 'core.base.exceptions.custom_exception_handler'
}

SWAGGER_SETTINGS = {
    "exclude_url_names": ['doc_swagger'],
    "exclude_namespaces": ['admin', 'doc_swagger'],
    "SECURITY_DEFINITIONS":
        {
            'Api Key': {"type": "apiKey", "name": "api-key", "in": "header"},
            'Bearer Token': {'type': 'apiKey', 'name': 'Bearer', 'in': 'header'},
        },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    "is_authenticated": False,
}

LOGGING = {
    'version': 1,  # Version del Gestor de Registros
    'disable_existing_loggers': False,  # Deshabilitar los registros predeterminados
    'filters': {
        # 'telegram_filter': 'logging.TelegramLogFilter',
    },
    'handlers': {  # Configurar los gestores
        'file': {
            'class': 'logging.FileHandler',
            'filename': env('LOG_FILE', default='app.log'),
            'formatter': 'verbose'
        },
        'telegram': {
            'class': 'custom.logging.TelegramLogHandler',
            'channel': env('TELEGRAM_CHANNEL', default=None),
            'token': env('TELEGRAM_TOKEN', default=None),
            'level': 'ERROR',
            'formatter': 'telegram-format',
            # 'filters': ['telegram_filter']
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['file', 'telegram'],
        },
    },
    'formatters': {
        'verbose': {
            'format': '{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'telegram-format': {
            'class': 'custom.logging.TelegramFormater'
        }
    },
}

Q_CLUSTER = {
    'name': 'CanteraJovenCUJAE',
    'workers': 1,
    'timeout': 60,
    'recycle': 500,
    'compress': True,
    'queue_limit': 500,
    'save_limit': 250,
    'max_attempts': 3,
    'label': 'Tareas de Cantera Joven CUJAE',
    'orm': 'default'
}

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL ', default=None)
EMAIL_HOST = env('EMAIL_HOST', default=None)
EMAIL_PORT = env('EMAIL_PORT', default=None)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default=None)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True)

SIGENU_URL = env('SIGENU_URL', default=None)
SIGENU_USERNAME = env('SIGENU_USERNAME', default=None)
SIGENU_PASSWORD = env('SIGENU_PASSWORD', default=None)

PFI_UPLOAD_ROOT = MEDIA_ROOT + '/plan-individual'
PFC_UPLOAD_ROOT = MEDIA_ROOT + '/plan-colectivo'

# apps_loader = AppsLoader()
# apps_loader.load()
# INSTALLED_APPS += apps_loader.get_apps()
