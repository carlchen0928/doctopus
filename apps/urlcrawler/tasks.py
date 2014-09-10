# -*- coding: utf-8 -*-
from celery import Celery
from celery.utils.log import get_task_logger
import pyreBloom
import tldextract
import time
import redis
from django.conf import settings

from utils import Fetch_and_parse_and_store

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Celery('tasks', broker='redis://172.21.1.155',
        backend='redis://172.21.1.155', 
		include=['apps.urlcrawler.tasks'],)
logger = get_task_logger(__name__)

@app.task
def retrieve_page(task_id, url, from_url=None, depth=0, now_depth=0, allow_domains=None):

    # Filter the url that has been crawled
    p = pyreBloom.pyreBloom('task%d' % task_id, 100000, 0.01, host='172.21.1.155')
    #if p.contains(url):
    #    return

	# start crawling...
	fps = Fetch_and_parse_and_store(task_id, url, from_url, \
            depth, now_depth, allow_domains, __name__)
	p.extend(url)
	
	if fps.fetch() == True:
		fps.store()
		fps.follow_links()
    # start crawling...
    fps = Fetch_and_parse_and_store(task_id, url, from_url, depth, 
            now_depth, allow_domains, __name__)
    p.extend(url)

    
    if fps.fetch() == True:
        fps.follow_links()
        if fps.store() == True:
            return settings.CELERY_WORKER_OK
        else:
            return settings.CELERY_WORKER_STOREE
    else:
        return settings.CELERY_WORKER_FETCHE
        

            
        



@app.task
def task_running():
    try:
        r = redis.Redis(connection_pool=settings.REDIS_POOL)
        running = r.hlen(REDIS_RUNNING)

        #if running task is very little, get some from queueing
        if running < REDIS_RUNNING_MAX:
            if r.llen(REDIS_QUEUEING) == 0:
                logger.debug('there is no queueing task!')
                return
            for i in range(1, REDIS_RUNNING_MAX - running):
                task = r.rpop(REDIS_QUEUEING)
                r.hset(REDIS_RUNNING, hash(task[0]), task)
                #split task into many urls and do work
                dispatch_task(task)
                logger.debug('task %s have been sent to running queue.' %
                        (task[0]))

    except Exception, e:
        logger.debug(e)
        logger.debug('can not push task from queueing to running')

@app.task
def task_complete(status, task_id, url):
    if status 
    print 'call task complete'


@app.task
def task_error(uuid, task_id, url):
    print 'call task error'


@app.task
def allTask_complete(task_id):
    #remove bloom filter
    #remove task from redis running
    #change mysql status
    #remove redis task-url dict
    print 'call allTask complete'
