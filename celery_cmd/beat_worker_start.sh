python manage.py celery -A apps.urlcrawler.tasks worker -Q task_running --loglevel INFO
