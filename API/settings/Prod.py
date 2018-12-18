from API.settings import Globals
from API.settings.Base import Base
from os.path import join


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
    Base.ALLOWED_HOSTS.append(ENGINE_HOSTNAME)
    Base.ALLOWED_HOSTS.append("52.25.200.16")
    Base.ALLOWED_HOSTS.append("*")
    STATIC_ROOT = join("/var", "www", "html", "incamedical", "INCAMedical_web", "media", )
    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"

    STATIC_URL = '/static/'
    # Additional locations of static files
    STATICFILES_DIRS = (
        join("/var", "www", "html", "incamedical", "INCAMedical", "static", ),
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )
