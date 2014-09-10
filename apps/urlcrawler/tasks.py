# -*- coding: utf-8 -*-
from celery import Celery
from celery.utils.log import get_task_logger
import pyreBloom
import tldextract
import time

from utils import Fetch_and_parse_and_store
from django.conf import settings

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
    fps = Fetch_and_parse_and_store(task_id, url, from_url, depth, 
            now_depth, allow_domains, __name__)
    p.extend(url)

    
    if fps.fetch() == True:
        fps.follow_links()
        if fps.store() == True:
            return settings.CELERY_WORKER_RESULT['successful']
        else:
            return settings.CELERY_WORKER_RESULT['store_error']
    else:
        return settings.CELERY_WORKER_RESULT['fetch_error']
        

            
        

	
