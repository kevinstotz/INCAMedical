#!/bin/bash

export DJANGO_SETTINGS_MODULE=API.settings.prod
export DJANGO_SERVER_TYPE=prod
export PYTHONPATH=/var/www/html/incamedical/INCAMedical
export SECRET_KEY="432432432fsd"

cd /var/www/html/incamedical/INCAMedical

/usr/local/bin/python /var/www/html/incamedical/INCAMedical/manage.py runserver 172.31.2.86:10100
