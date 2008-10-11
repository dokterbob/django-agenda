#!/usr/local/bin/bash

if [ -f /usr/local/bin/use-django ]; then
    source /usr/local/bin/use-django
    use-django r9067
fi

PWD=`pwd`
BASEPATH=`basename $PWD`
if [[ $1 != "" ]]; then
    python manage.py $1
else
    screen -S $BASEPATH python manage.py runserver `hostname`:7483
fi

