# -*- coding: utf-8 -*-
DEBUG = False
TEMPLATE_DEBUG = DEBUG

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = 1
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'

USE_I18N = True
USE_L10N = True
USE_TZ = False
USE_THOUSAND_SEPARATOR = True

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.formtools',
    'crispy_forms',
    'waffle',
    # App
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

STATIC_URL = '/static/'

GRAPPELLI_ADMIN_TITLE = 'App'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..', 'media'))
MEDIA_URL = '/media/'

FIXTURE_DIRS = ()

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

BROKER_TRANSPORT = 'django'

from django.contrib.messages import constants
MESSAGE_TAGS = {
    constants.ERROR: 'danger',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'info@app.ru'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console':{
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'app.base': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO'
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-cache',
    },
    'core-cache': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'core-cache',
        'TIMEOUT': 60
    }
}
