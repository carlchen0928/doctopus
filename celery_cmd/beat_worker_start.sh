screen -S beat_worker python manage.py celery -A apps.urlcrawler.tasks worker -Q task_running --loglevel DEBUG
