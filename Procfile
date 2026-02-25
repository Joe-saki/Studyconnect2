release: python manage.py migrate
web: gunicorn studyconnect.wsgi:application --bind 0.0.0.0:$PORT
