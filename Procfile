web: gunicorn loans_for_good.wsgi:application --log-file -
worker: celery -A loans_for_good worker --loglevel=info
