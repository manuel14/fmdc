from .default import *

# Do not use this on production. This is a mockup
SECRET_KEY = 'THISISONLYAMOCKUPSECRETKEYBUTWORKSANYWAYS'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Mail developer
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587


INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
    'bootstrap3',
    'django_cleanup',
    'nested_admin',
    'tinymce',
]
