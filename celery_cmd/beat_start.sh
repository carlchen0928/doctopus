#-----Starting the Scheduler-----
python manage.py celery -A apps.urlcrawler.tasks beat --loglevel INFO #--logfile tmp.log
