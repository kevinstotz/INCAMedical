from API.settings.Base import Base
from API.settings import Globals
from os.path import join


class Dev(Base):
    DEBUG = True
    DJANGO_LOG_LEVEL = DEBUG

    WEBSITE_IP_ADDRESS = "127.0.0.1"
    WEBSITE_HOSTNAME = 'www.www.incamedical.com'
    WEBSITE_PORT = 10102

    DASHBOARD_IP_ADDRESS = "127.0.0.1"
    DASHBOARD_HOSTNAME = 'www.audits.incamedical.com'
    DASHBOARD_PORT = 10101

    ENGINE_IP_ADDRESS = "127.0.0.1"
    ENGINE_DOMAIN = 'incamedical.com'
    ENGINE_HOSTNAME = 'www.api.' + ENGINE_DOMAIN
    ENGINE_PORT = 10100

    WEBSITE_HOSTNAME_AND_PORT = WEBSITE_HOSTNAME + ":" + str(WEBSITE_PORT)
    WEBSITE_HOSTNAME_URL = Globals.UNSECURE + WEBSITE_HOSTNAME + ":" + str(WEBSITE_PORT)

    DASHBOARD_HOSTNAME_AND_PORT = DASHBOARD_HOSTNAME + ":" + str(DASHBOARD_PORT)
    DASHBOARD_HOSTNAME_URL = Globals.UNSECURE + DASHBOARD_HOSTNAME + ":" + str(DASHBOARD_PORT)

    ENGINE_HOSTNAME_NO_PORT = Globals.UNSECURE + ENGINE_HOSTNAME
    ENGINE_HOSTNAME_AND_PORT = ENGINE_HOSTNAME + ":" + str(ENGINE_PORT)
    ENGINE_HOSTNAME_URL = Globals.UNSECURE + ENGINE_HOSTNAME + ":" + str(ENGINE_PORT)

    Base.ALLOWED_HOSTS.append(WEBSITE_HOSTNAME)
    Base.ALLOWED_HOSTS.append(ENGINE_HOSTNAME)
    Base.ALLOWED_HOSTS.append(DASHBOARD_HOSTNAME)

    Base.CORS_ORIGIN_WHITELIST.append(WEBSITE_IP_ADDRESS)
    Base.CORS_ORIGIN_WHITELIST.append(WEBSITE_HOSTNAME)
    Base.CORS_ORIGIN_WHITELIST.append(DASHBOARD_HOSTNAME_URL)
    Base.CORS_ORIGIN_WHITELIST.append("http://www.audits.incamedical.com:10101")
    Base.CORS_ORIGIN_WHITELIST.append("http://www.api.incamedical.com:10101")

    Base.CSRF_TRUSTED_ORIGINS.append(WEBSITE_HOSTNAME)
    Base.CSRF_TRUSTED_ORIGINS.append(WEBSITE_IP_ADDRESS)
    Base.CSRF_TRUSTED_ORIGINS.append(DASHBOARD_HOSTNAME_URL)
    Base.CSRF_TRUSTED_ORIGINS.append("http://www.audits.incamedical.com:10101")
    Base.CSRF_TRUSTED_ORIGINS.append("http://www.api.incamedical.com:10101")

    Base.DATABASES = {
        'default': {
            'NAME': 'incamedicalapi_dev',
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'read_default_file': join('c:/', 'ProgramData', 'MySQL', 'MySQL Server 5.7', 'mysql.incamedical.ini'),
            },
        },

    }
