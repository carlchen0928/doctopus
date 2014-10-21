python manage.py celery -A apps.urlcrawler.tasks worker -Q url_crawler --loglevel DEBUG
