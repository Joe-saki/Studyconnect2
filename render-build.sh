#!/bin/bash
set -o errexit

pip install -r requirements.txt

# Run manage.py commands from the correct location
if [ -f manage.py ]; then
	python manage.py collectstatic --noinput
	python manage.py migrate
elif [ -f studyconnect/manage.py ]; then
	cd studyconnect
	python manage.py collectstatic --noinput
	python manage.py migrate
else
	echo "manage.py not found"
	exit 1
fi
