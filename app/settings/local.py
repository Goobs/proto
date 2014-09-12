# -*- coding: utf-8 -*-
from base import *

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ('localhost', )

SECRET_KEY = 'dugzb0gwyj!02$3wq)b)23bel5ai@0m4j=^l%ybsdvs_q=lb&l'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'app.db'),
    }
}

APPS = (
    'app.accounts',
    'app.landing',

)

INSTALLED_APPS += APPS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if 'app.accounts' in APPS:
    AUTH_USER_MODEL = 'accounts.User'

ROBOKASSA_LOGIN = 'othercamp'
ROBOKASSA_PASSWORD1 = 'otherpass1'
ROBOKASSA_PASSWORD2 = 'otherpass2'
ROBOKASSA_TEST_MODE = True

""" COCCOC " ""

LANGUAGE_CODE = 'en'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/'

SOCIAL_AUTH_USER_MODEL = 'core.User'

FACEBOOK_APP_ID = '522163924560793'
FACEBOOK_API_SECRET = '8cb2e2dafa8a2ddcc15630fafc227f03'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

TWITTER_CONSUMER_KEY = '7XQ5kiLYG3nfpjzng908g'
TWITTER_CONSUMER_SECRET = 'ikmV5xJIssnBFJXFSglmq3CXxKKiq5Tmm2EvQEAjvY'

GOOGLE_OAUTH2_CLIENT_ID = '99949687708-o1ik9ikp7qhaopsfma1shonn25a8ck5k.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = '33BZhLjlKJ7SsD4KdlSnCzB2'

" "" / COCCOC """
