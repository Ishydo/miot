#!/bin/bash

python3 manage.py migrate
python3 manage.py loaddata sites
python3 manage.py loaddata categories
python3 manage.py loaddata templates

echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('miot@miot.miot', 'miotuser', 'password')" | python manage.py shell

python3 manage.py runserver 0.0.0.0:8000
