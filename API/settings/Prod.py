from API.settings import Globals
from API.settings.Base import Base
from os import environ


class Prod(Base):
    TIME_ZONE = 'UTC'

    # SECURITY WARNING: don't run with debug turned on in production!

    WEBSITE_IP_ADDRESS = "127.0.0.1"
    WEBSITE_DOMAIN = 'incamedical.com'
    WEBSITE_HOSTNAME = 'audits' + "." + WEBSITE_DOMAIN
    WEBSITE_HOSTNAME_PORT = 10101
    WEBSITE_HOSTNAME_URL = WEBSITE_HOSTNAME + ":" + str(WEBSITE_HOSTNAME_PORT)

    ENGINE_IP_ADDRESS = "127.0.0.1"
    ENGINE_DOMAIN = 'incamedical.com'
    ENGINE_HOSTNAME = 'api' + "." + ENGINE_DOMAIN
    ENGINE_HOSTNAME_PORT = 10100
    ENGINE_HOSTNAME_URL = Globals.UNSECURE + ENGINE_HOSTNAME + ":" + str(ENGINE_HOSTNAME_PORT)

    # SECRET_KEY = environ['SECRET_KEY']
    Base.ALLOWED_HOSTS.append(WEBSITE_HOSTNAME)
