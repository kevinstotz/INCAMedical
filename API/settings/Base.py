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
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

class Base(Configuration):
    SECRET_KEY = Globals.SECRET_KEY

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = [
        'corsheaders',
        'rest_framework',
        'rest_framework_filters',
        'django_user_agents',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'API.apps.APIConfig',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django_user_agents.middleware.UserAgentMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    REST_FRAMEWORK = {
        #  'PAGE_SIZE': 10,
        'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
        'DEFAULT_FILTER_BACKENDS': ('rest_framework_filters.backends.RestFrameworkFilterBackend',
                                    'rest_framework.filters.SearchFilter',
                                    'rest_framework.filters.OrderingFilter', ),
        'DEFAULT_PAGINATION_CLASS':
            'rest_framework_json_api.pagination.PageNumberPagination',
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework_json_api.parsers.JSONParser',
            'rest_framework.parsers.MultiPartParser',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework_json_api.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    }
    CORS_ORIGIN_WHITELIST = []
    CSRF_TRUSTED_ORIGINS = []

    CORS_ORIGIN_ALLOW_ALL = True

    CORS_ALLOW_HEADERS = (
        'Content-Type',
        'Access-Control-Allow-Origin',
        'Accept',
        #  'Accept-Encoding',
        #   'x-requested-with',
        #   'x-csrftoken',
        #   'Content-Disposition',
        #   'Access-Control-Allow-Credentials',
        #   'Origin',
        #   'enctype',
        #   'user-agent',
        #   'Redirect',
        #   'Authorization',
    )

    #  CORS_ALLOW_CREDENTIALS = True

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
    MEDIA_URL = ''
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.1/howto/static-files/
    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"

    STATIC_ROOT = ''
    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"

    STATIC_URL = '/static/'
    # Additional locations of static files
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )
    ROOT_URLCONF = 'API.urls'

from API.settings.Dev import *
from API.settings.Prod import *
