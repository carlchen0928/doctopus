
python manage.py celery -A apps.urlcrawler.tasks worker -Q allTask_complete --loglevel DEBUG
