#!/bin/bash
PYTHON=`which python`
#python manage.py loaddata fixtures.json
$PYTHON manage.py loaddata mailserver.json
$PYTHON manage.py loaddata country.json
$PYTHON manage.py loaddata state.json
$PYTHON manage.py loaddata city.json
$PYTHON manage.py loaddata zipcode.json
$PYTHON manage.py loaddata userstatus.json
$PYTHON manage.py loaddata customuser.json
$PYTHON manage.py loaddata addresstype.json
$PYTHON manage.py loaddata address.json
$PYTHON manage.py loaddata nametype.json
$PYTHON manage.py loaddata personname.json
$PYTHON manage.py loaddata userprofile.json
$PYTHON manage.py loaddata company.json
$PYTHON manage.py loaddata specialtytype.json
$PYTHON manage.py loaddata clinictype.json
$PYTHON manage.py loaddata category.json
$PYTHON manage.py loaddata indicatortype.json
$PYTHON manage.py loaddata indicatoroption.json
$PYTHON manage.py loaddata indicator.json
$PYTHON manage.py loaddata template.json
$PYTHON manage.py loaddata templatecategory.json
$PYTHON manage.py loaddata templateindicator.json
$PYTHON manage.py loaddata phonenumbertype.json
$PYTHON manage.py loaddata phonenumber.json
$PYTHON manage.py loaddata auditarea.json
$PYTHON manage.py loaddata audit.json
$PYTHON manage.py loaddata notificationtype.json
$PYTHON manage.py loaddata notificationstatus.json
$PYTHON manage.py loaddata notification.json
$PYTHON manage.py loaddata emailtemplate.json
$PYTHON manage.py loaddata emailaddresstype.json
$PYTHON manage.py loaddata emailaddressstatus.json
$PYTHON manage.py loaddata emailaddress.json

