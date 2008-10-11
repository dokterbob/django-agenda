#!/usr/local/bin/bash
source /usr/local/bin/use-django
use-django r9067

PWD=`pwd`
BASEPATH=`basename $PWD`
if [[ $1 != "" ]]; then
    python manage.py $1
else
    screen -S $BASEPATH python manage.py runserver `hostname`:7483
fi

