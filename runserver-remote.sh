#!/bin/bash

PWD=`pwd`
BASEPATH=`basename $PWD`
if [[ $1 != "" ]]; then
    python manage.py 7483
else
    screen -S $BASEPATH python manage.py runserver `hostname`:7483
fi

