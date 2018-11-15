#!/bin/bash

export DJANGO_SETTINGS_MODULE=API.settings.Base
export PYTHONPATH=/var/www/html/incamedical/INCAMedical

cd /var/www/html/incamedical/INCAMedical

/usr/local/bin/python /var/www/html/incamedical/INCAMedical/manage.py runserver 172.31.2.86:10100  --configuration=Prod --settings=API.settings.Base

