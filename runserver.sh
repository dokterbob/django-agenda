#!/usr/local/bin/bash
source /usr/local/bin/use-django
use-django r9067
if [[ $1 != "" ]]; then
    python manage.py $1
else
	screen python manage.py runserver `hostname`:7483
fi

