#-----Starting the Scheduler-----
screen -S beat python manage.py celery -A apps.urlcrawler.tasks beat --loglevel DEBUG #--logfile tmp.log
