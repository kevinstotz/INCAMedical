from os.path import join, abspath, dirname, relpath, realpath

BASE_DIR = abspath(dirname(__name__))  # .../DimeAPI
PROJECT_DIR = dirname(dirname(abspath(__file__)))  # .../DimeAPI/DimeAPI
SETTINGS_DIR = dirname(realpath(__file__))  # .../DimeAPI/DimeAPI/settings
PROJECT_NAME = relpath(PROJECT_DIR)  # DimeAPI

SECURE = 'https://'
UNSECURE = 'http://'
SECRET_KEY = '(tlbv7h$1t9tono86(4w%aat9@%6*^#s7q)f1hojg#v8f&16ig'

# Email settings
TEMPLATE_COMPANY = 0
PASSWORD_LENGTH = 64
EMAIL_TIMEOUT = 10
EMAIL_LENGTH = 100
EMAIL_USE_TLS = True
EMAIL_TEMPLATE_DIR = join(PROJECT_NAME, "EmailTemplates")
EMAIL_FROM_DOMAIN = 'incamedical.com'
NONCE_LENGTH = 50
ADDRESS_LENGTH = 42
SITE_ID_LENGTH = 10
URL_LENGTH = 255
COMPANY_NAME_LENGTH = 255
AUDIT_AREA_NAME_LENGTH = 255
FIRST_NAME_LENGTH = 50
LAST_NAME_LENGTH = 50
AUTHORIZATION_CODE_LENGTH = 20
IMAGE_DIR = "images/"
ICON_NAME_LENGTH = 30
UUID_ZERO = "00000000-0000-0000-0000-000000000000"

USER_STATUS = {
    'ACTIVE': 1,
    'INACTIVE': 2,
    'SUSPENDED': 3,
    'BLOCKED': 4,
    'VISITOR': 5
}
NAME_TYPE = {
    'FIRST': 1,
    'LAST': 2,
    'MAIDEN': 3,
    'MIDDLE': 4,
    'NICKNAME': 5,
    'SALUTATION': 6,
    'SUFFIX': 7,
    'FULL': 8
}
#  Phone number Type
MOBILE, HOME, WORK, AUTO = range(1, 5)
PHONE_NUMBER_TYPE = (
    (MOBILE, 'Mobile'),
    (HOME, 'Home'),
    (WORK, 'Work'),
    (AUTO, 'Auto'),
)
#  Email Templates
EMAIL_TEMPLATE = {
    'VERIFY': 1,
    'WELCOME': 2,
    'FORGOT': 3,
    'RESET': 4,
    'CONTACTUS': 5,
    'AFFILIATE': 6
}
EMAIL_ADDRESS_TYPE = {
    'PRIMARY': 1,
    'SECONDARY': 2
}
EMAIL_ADDRESS_STATUS = {
    'ACTIVE': 1,
    'INACTIVE': 2,
    'SUSPENDED': 3,
    'BLOCKED': 4,
    'EXISTS': 5,
    'NOTFOUND': 6
}
ADDRESS_TYPE = {
    'HOME': 1,
    'MAILING': 2,
    'WORK': 3
}
NOTIFICATION_TYPE = {
    'EMAIL': 1,
    'TEXT': 2,
    'PHONE': 3
}
#  Notification Status
NOTIFICATION_STATUS = {
    'READY': 1,
    'QUEUED': 2,
    'SENT': 3,
    'FAILED': 4
}