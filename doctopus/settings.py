"""
Django settings for doctopus project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import redis
from mongoengine import connect
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates').replace('\\', '/'),
)
FILE_DIRS = os.path.join(BASE_DIR, 'urlfiles').replace('\\', '/')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+6v-pc*7ja&-8mc9erp%-8#=qzm#%uy_+avawh@kujj!0sr0r7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
import djcelery
djcelery.setup_loader()

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.urlcrawler', 
	'djcelery'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'doctopus.urls'

WSGI_APPLICATION = 'doctopus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'doctopus',
        'USER': 'xli', 
        'PASSWORD': '123456', 
        'HOST': '172.21.1.151',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
)



#================
#===== Mongo ====
#================

MONGO_DB = {
    'host': '172.21.1.155:27017', 
    'name': 'doctopus',
}

MONGO_DB_DEFAULTS = {
    'name': 'doctopus', 
    'host': '172.21.1.155:27017', 
    'alias': 'default', 
}

MONGO_DB = dict(MONGO_DB_DEFAULTS, **MONGO_DB)

MONGODB = connect(MONGO_DB.pop('name'), **MONGO_DB)


#===============================
#======== Celery ===============
#===============================
(CELERY_WORKER_OK, \
 CELERY_WORKER_FETCHE, \
 CELERY_WORKER_STOREE, \
 CELERY_WORKER_RUNNING) = range(1, 5)

BROKER_URL = 'redis://172.21.1.155/9'
CELERY_RESULT_BACKEND = 'redis://172.21.1.155/10'

DOWNLOAD_DELAY = 300


#====================
#=== Task Result  ===
#====================
(TASK_FINISH, \
 TASK_FINISH_WITH_ERROR) = range(1, 3)

#===============
#===  REDIS ====
#===============
REDIS = {
    'host': '172.21.1.155',
}

REDIS_POOL = redis.ConnectionPool(host=REDIS['host'], port=6379, db=9)

REDIS_QUEUEING_MAX = 1500
REDIS_RUNNING_MAX = 10
REDIS_QUEUEING = 'UserTask_Queueing'
REDIS_RUNNING = 'UserTask_Running'


#===================================
#========== Celery Beat ============
#===================================
from datetime import timedelta
CELERY_IMPORTS = ("apps.urlcrawler.tasks",)
CELERY_INCLUDE = ("apps.urlcrawler.tasks",)

CELERYBEAT_SCHEDULE = {
    "check_running_queue": {
        "task": "apps.urlcrawler.tasks.task_running",
        "schedule": timedelta(seconds=10),
    },
}
#=====================================
#=========== Routing task ============
#=====================================
CELERY_ROUTES = {
    'apps.urlcrawler.tasks.task_running': {
        'queue': 'task_running',
    },
    'apps.urlcrawler.tasks.new_task': {
        'queue': 'new_task',
    },
    'apps.urlcrawler.tasks.task_complete': {
        'queue': 'task_complete',
    },
    'apps.urlcrawler.tasks.allTask_complete': {
        'queue': 'allTask_complete',
    },
    'apps.urlcrawler.tasks.retrieve_page': {
        'queue': 'url_crawler',
    },
}

#CELERY_QUEUES = {
#    'task_running': {
#        'exchange': 'task_running',
#        'exchange_type': 'direct',
#        'binding_key': 'task_running',
#    },
#}
