#!/bin/bash
PYTHON=`which python`
python manage.py loaddata --configuration=Prod --settings=API.settings.Base image.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base index.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base role.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base permission.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base mailserver.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base country.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base state.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base city.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base zipcode.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base userstatus.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base userprofile.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base customuser.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base company.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base addresstype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base address.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base upload.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base uploadtype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base notetype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base note.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base nametype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base personname.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base company.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base specialtytype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base clinictype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base category.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base indicatortype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base indicatoroption.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base indicator.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base template.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base templatecategory.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base templateindicatortype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base templateindicatoroption.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base templateindicator.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base auditarea.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base audit.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base phonenumbertype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base phonenumber.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base notificationtype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base notificationstatus.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base notification.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base emailtemplate.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base emailaddresstype.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base emailaddressstatus.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base emailaddress.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base auditindicatorupload.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base auditindicatornote.json
python manage.py loaddata --configuration=Prod --settings=API.settings.Base auditindicatoroption.json

