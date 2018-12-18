#!/bin/bash
set DJANGO_CONFIGURATION=Prod
export DJANGO_CONFIGURATION
set DJANGO_SERVER_TYPE=API.settings.Base
export DJANGO_SERVER_TYPE
set DJANGO_SETTINGS_MODULE=API.settings.Base
export DJANGO_SETTINGS_MODULE
set PYTHONPATH=/var/www/html/incamedical/INCAMedical
export PYTHONPATH

cd /var/www/html/incamedical/INCAMedical

/usr/local/bin/python3 /var/www/html/incamedical/INCAMedical/manage.py runserver 172.31.2.86:10100  --configuration=Prod --settings=API.settings.Base --pythonpath=/var/www/html/incamedical/INCAMedical >> /tmp/api.out

