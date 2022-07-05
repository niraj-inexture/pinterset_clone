release: python manage.py migrate
web: gunicorn pinterest.wsgi
web: daphne pinterest.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker --settings=pinterest.settings -v2