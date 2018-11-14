from os.path import join
from os import environ
from API.settings.base import *


SECRET_KEY = environ['SECRET_KEY']
ROOT_URLCONF = 'API.urls'
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'NAME': 'INCAMedical',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'dev.cdt994n5tnkz.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': join('/', 'etc/', 'mysql/', 'conf.d/', 'mysql.INCAMedical.cnf'),
        },

    },
}

try:
    from .local import *
except ImportError:
    local = None
    raise ImportError('local settings import not found')
