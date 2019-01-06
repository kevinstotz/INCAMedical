"""
Django settings for API project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from configurations import Configuration
from API.settings import Globals
from os.path import join
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


class Base(Configuration):
    SECRET_KEY = Globals.SECRET_KEY

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'corsheaders',
        'oauth2_provider',
        'rest_framework',
        'rest_framework_filters',
        'django_user_agents',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'API.apps.APIConfig',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django_user_agents.middleware.UserAgentMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    OAUTH2_PROVIDER = {
        # this is the list of available scopes
        'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
    }

    AUTHENTICATION_BACKENDS = (
        'oauth2_provider.backends.OAuth2Backend',
        'rest_framework.authentication.SessionAuthentication',
        'django.contrib.auth.backends.ModelBackend',

        # Uncomment following if you want to access the admin
    )
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_SAVE_EVERY_REQUEST = True
    SESSION_COOKIE_AGE = 86400  # sec
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_NAME = 'DSESSIONID'
    SESSION_COOKIE_SECURE = False
    REST_FRAMEWORK = {
        #  'PAGE_SIZE': 10,
        'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
        'DEFAULT_FILTER_BACKENDS': ('rest_framework_filters.backends.RestFrameworkFilterBackend',
                                    'rest_framework.filters.SearchFilter',
                                    'rest_framework.filters.OrderingFilter', ),
        'DEFAULT_PAGINATION_CLASS':
            'rest_framework_json_api.pagination.PageNumberPagination',
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated'
        ),
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework_json_api.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework_json_api.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    }

    CORS_ORIGIN_WHITELIST = ("www.www.incamedical.com:10101", "http://www.www.incamedical.com:10101")

    CORS_ORIGIN_ALLOW_ALL = True

    CORS_ALLOW_HEADERS = (
        'Content-Type',
        'contentType',
        'Access-Control-Allow-Origin',
        'Accept',
        #  'Accept-Encoding',
        #   'x-requested-with',
        # 'x-csrftoken',
        #   'Content-Disposition',
        #   'Access-Control-Allow-Credentials',
        #   'Origin',
        'enctype',
        #   'user-agent',
        #   'Redirect',
        'Authorization',
    )

    CORS_ALLOW_CREDENTIALS = True

    CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS',
    )
    ROOT_URLCONF = 'API.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    # Database
    # https://docs.djangoproject.com/en/2.1/ref/settings/#databases

    DATABASES = {
        'default': {
            'NAME': 'INCAMedical',
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'dev.cdt994n5tnkz.us-west-2.rds.amazonaws.com',
            'PORT': '3306',
            'OPTIONS': {
                'read_default_file': join('/etc', 'mysql', 'conf.d', 'mysql.INCAMedical.cnf'),
            },

        },
    }
    # Password validation
    # https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/2.1/topics/i18n/
    ADMINS = (
        ('Kevin Admin', 'kevin_stotz@yahoo.com'),
    )

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    AUTH_USER_MODEL = 'API.CustomUser'
    MANAGERS = ADMINS
    # base public URL of MEDIA_ROOT directory
    MEDIA_URL = join('static', 'media/')
    MEDIA_ROOT = join(Globals.BASE_DIR, 'media')

    STATIC_URL = '/static/'
    #  STATIC_ROOT = join(Globals.BASE_DIR, "API", "static")
    STATIC_ROOT = Globals.BASE_DIR.child('static')
    STATICFILES_DIRS = [
        Globals.BASE_DIR.child('API').child('static'), ]

# from API.settings.Prod import Prod
from API.settings.Dev import Dev
