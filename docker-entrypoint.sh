#!/bin/bash

apt-get update
apt-get install nodejs npm

ln -s /usr/bin/nodejs /usr/local/bin/node
ln -s /usr/bin/npm /usr/local/bin/npm

npm install
node_modules/.bin/webpack --config webpack.config.js

python3 manage.py migrate
python3 manage.py loaddata sites
python3 manage.py loaddata categories
python3 manage.py loaddata templates
python3 manage.py loaddata socialapps

echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('miot@miot.miot', 'miotuser', 'password')" | python manage.py shell

python3 manage.py runserver 0.0.0.0:8000
