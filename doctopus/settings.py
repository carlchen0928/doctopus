"""
Django settings for doctopus project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from mongoengine import connect
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+6v-pc*7ja&-8mc9erp%-8#=qzm#%uy_+avawh@kujj!0sr0r7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

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
import djcelery
djcelery.setup_loader()

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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


REDIS = {
    'host': '172.21.1.155'
}


#===============
#===  REDIS ====
#===============
REDIS = {
    'host': '172.21.1.155',
}

REDIS_POOL = redis.ConnectionPool(host=REDIS['host'], port=6379, db=9)

REDIS_QUEUEING_MAX = 1500
REDIS_RUNNING_MAX = 10
REDIS_QUEUEING = 'task_queueing'
REDIS_RUNNING = 'task_running'

