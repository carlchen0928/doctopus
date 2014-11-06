# -*- coding: utf-8 -*-
from celery import Celery
from celery.utils.log import get_task_logger
import pyreBloom
import tldextract
import time
import os
import redis
import base64
import binascii
import acker
import tasks
import pickle
import traceback
from django.conf import settings
from datetime import timedelta
from apps.urlcrawler.models import runningTask
from apps.urlcrawler.models import urlTask 

from utils import Fetch_and_parse_and_store, dispatch_task

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#=================Celery App===============================
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
app = Celery('tasks')
app.config_from_object('django.conf:settings')#Important
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#===========================================================

logger = get_task_logger(__name__)

@app.task
def retrieve_page(task_id, url, from_url=None, depth=0, now_depth=0, allow_domains=None):

    # Filter the url that has been crawled
    logger.error('-------------------' + str(depth))
    url = url.strip()

    # start crawling...
    fps = Fetch_and_parse_and_store(task_id, url, from_url, depth, 
            now_depth, allow_domains, __name__)

    proxies = {
        'http': settings.COW_PROXY_HANDLER, 
        'https': settings.COW_PROXY_HANDLER,
    }

    if fps.fetch(proxies=proxies) == True:
        logger.warning('Before fps.follow_links()')
        fps.follow_links()
        logger.warning('After fps.follow_links()')
        logger.warning('CALL STORE................')
        if fps.store() == True:
            logger.info('%s OK!' % (url))
            return settings.CELERY_WORKER_OK
        else:
            logger.error('%s STORE ERROR!' % (url))
            return settings.CELERY_WORKER_STOREE
    else:
        logger.error('%s FETCH ERROR!' % (url))
        return settings.CELERY_WORKER_FETCHE


# This task run in the server
# handling the task in Redis Queue--->run
@app.task
def task_running():
    try:
        r = redis.Redis(connection_pool=settings.REDIS_POOL)
        running = r.hlen(settings.REDIS_RUNNING)

        #if running task is very little, get some from queueing
        if running < settings.REDIS_RUNNING_MAX:
            length = r.llen(settings.REDIS_QUEUEING)
            if length == 0:
                logger.info('there is no queueing task!')
                return
            smaller = min(length, settings.REDIS_RUNNING_MAX - running) 
            for i in range(smaller):
                task = r.rpop(settings.REDIS_QUEUEING)
                task = pickle.loads(task)

                r.hset(settings.REDIS_RUNNING, hash(task[0]),
                        pickle.dumps(task))
                urlTask.objects.filter(task_id=task[0]).update(status='Running')
                
                #split task into many urls and do work
                dispatch_task(task, __name__, r)
                logger.info('task %s have been sent to running queue.' %
                        (task[0]))

    except Exception, e:
        traceback.print_exc()
        logger.error('can not push task from queueing to running')

'''
@app.task
def task_complete(status, task_id, url):
    r = redis.Redis(connection_pool=settings.REDIS_POOL)
    if not r.exists('mp_' + task_id):
        logger.error('task %s map not exist in redis!' % (task_id))
        return
    r.hset(hash(url), status)
    print 'call task complete'
'''

@app.task
def task_error(uuid, task_id, url):
    print 'call task error'
    pass

# This task run in server
# handling the url follewed the seed url
@app.task
def new_task(task_id, url):
    #write task_id, url to mysql
    #xor with url
    logger.warning('new task started. URL: %s' % (url))
    taskr = runningTask(task_id=task_id, page_url=url)
    taskr.save()
    try:
        acker.setValue(task_id, url)
    except Exception, e:
        traceback.print_exc()
        logger.error(e)
        logger.error('encode error with task %s url %s' % (task_id, url))


# This task run in server
# handling the url completed
@app.task
def task_complete(ret_val, task_id, url):
    #xor this url
    #check xor value zero
    #if done, call allTask_complete
    try:
        acker.setValue(task_id, url)
    except Exception, e:
        traceback.print_exc()
        logger.error(e)
        logger.error('encode error with task %s url %s' % (task_id, url))
        return
    if ret_val == settings.CELERY_WORKER_OK:
        logger.info('DELETE FROM DATABASE WHERE URL=%s' % (url))
        runningTask.objects.filter(task_id=task_id, page_url=url).delete()
    else:
        logger.error('RETURN VALUE EQUALS %d' % (ret_val))

    xorValue = 1
    try:
        xorValue = acker.getValue(task_id)
    except Exception, e:
        traceback.print_exc()
        logger.error(e)
        logger.error('get xor value error with task %s'% (task_id))
        return

    if int(xorValue) == 0:
        result = allTask_complete.delay(task_id)        
        result.get()
        logger.info('task %s have done!' % (task_id))


# This task run in server
@app.task
def allTask_complete(task_id):
    #remove bloom filter
    #remove task from redis running
    #change mysql status
    #remove redis task-url dict
    print 'call allTask complete'
    p = pyreBloom.pyreBloom('task%s' % (task_id), 100000, 0.01, host='172.21.1.155')
    p.delete()
    r = redis.Redis(connection_pool=settings.REDIS_POOL)
    r.hdel(settings.REDIS_RUNNING, hash(task_id))
    r.hdel('task_xor', task_id)
    urlTask.objects.filter(task_id=task_id).update(status='Completed')
