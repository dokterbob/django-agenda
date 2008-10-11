#!/bin/bash

cd `dirname $BASH_SOURCE`

PWD=`pwd`
BASEPATH=`basename $PWD`

if [ ! -f portnumber ]; then
    echo 'No port number set!'
    echo 'Please create a file named "portnumber" in the current directory with'
    echo 'a locally unique portnumber in it, like "1234".'
    exit -1
fi

if [[ $1 != "" ]]; then
    python manage.py $1
else
    screen -S $BASEPATH python manage.py runserver `hostname`:`cat portnumber`
fi

