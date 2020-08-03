#! /bin/sh

python manage.py makemigrations user &&\
python manage.py migrate user --fake &&\
python manage.py makemigrations traceable &&\
python manage.py migrate traceable &&\
python manage.py runserver 0.0.0.0:8000

exec "$@"
