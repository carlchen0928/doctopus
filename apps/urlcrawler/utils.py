#-*- coding: utf-8 -*-

import datetime
import time
import requests
import urlparse
import tasks
import redis
import pickle
import acker
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger
from apps.urlcrawler.models import DDoc
from django.conf import settings


def dispatch_task(task, log_name, r):
    logger = get_task_logger(log_name)

    task_id = task[0]
    url_path = task[1]
    max_depth = task[2]
    allow_domains = task[3]
    urls = []
    
    #check the argument
    if task_id == None:
        logger.error('task_id is None.')
        return
    if url_path == None:
        logger.error('url_path is None.')
        return
    if max_depth == None:
        logger.error('max_depth is None.')
        return
    elif max_depth < 0:
        logger.debug('max depth less than ZERO, set it to ZERO.')
        max_depth = 0
    logger.info(task)
    logger.info(task[1])

    try:
        with open(url_path, 'r') as f:
            urls = f.readlines()
    except Exception, e:
        logger.error(e)
        return
    if urls == []:
        logger.error('url list is empty, can not continue')
        return
        
    #make a dict in redis, to track this task's status, use xor value.
    r.hset('task_xor', task_id, 0)

    for url in urls:
        logger.info(url)
        #start celery task
        #ack task
        url = url.strip()
        acker.setValue(task_id, url)
        tasks.retrieve_page.apply_async((task_id, url, \
                    None, max_depth, 0,\
                    allow_domains), \
                    link=tasks.task_complete.s(task_id, url))
        logger.info('task %d\'s url: %s has been sent.' % (task_id, url))



class Fetch_and_parse_and_store(object):
	
    def __init__(self, task_id, url, from_url, depth, now_depth, allow_domains, log_name):
        self.task_id = task_id
        self.url = url
        self.from_url = from_url
        self.depth = depth
        self.now_depth = now_depth
        self.allow_domains = allow_domains

        self.parse_url()

        self.page_source = ''
        self.custom_headers()

        self.logger = get_task_logger(log_name)

    def fetch(self, retry=2, proxies=None):
		
        try:
            response = requests.get(self.url, \
                    headers=self.headers, proxies=proxies)
            if self.is_response_avaliable(response):
                self.logger.info(self.url)
                self.page_source = response.text
                return True
            else:
                self.logger.warning('Page not avaliable. Status code: %d URL:%s' \
                        % (response.status_code, self.url))
                return False
        except Exception, e:
            #if retry > 0:
                #return self.fetch(retry - 1, proxies=proxies)
            #else:
            self.logger.error('FROM URL: %s' % (self.from_url))
            self.logger.error(str(e) + ' URL: %s' % self.url)
            return False

    def follow_links_delay(self, href, sleep_or_not):
        self.logger.warning('Before delay get')
        tasks.new_task.delay(self.task_id, href).get()
        self.logger.warning('After delay get')

        tasks.retrieve_page.apply_async((self.task_id, href, self.url, \
            self.depth, self.now_depth + 1, self.allow_domains), \
            link=tasks.task_complete.s(self.task_id, href))
        self.logger.info('DESPATCH A TASK URL=%s' % (href))

        if sleep_or_not == 1:
    		time.sleep(settings.DOWNLOAD_DELAY / 60)


	# be supposed to earse the links to photo, css and js.
    def follow_links(self):
        if self.now_depth >= self.depth:
            return

        soup = BeautifulSoup(self.page_source)
        for link in soup.find_all('a', href=True):
            href = link.get('href').encode('utf8')
            if not href.startswith('http'):
                href = urlparse.urljoin(self.url, href)
                self.follow_links_delay(href, 1)
            elif href.find(self.netloc) != -1:
                self.follow_links_delay(href, 1)
            else:
                for domain in self.allow_domains:
                    if href.find(domain) != -1:
                        self.follow_links_delay(href, 0)
                        break

    def store(self):
        #self.page_source, self.url
        #task_complete.delay(settings.CELERY_WORKER_OK, self.task_id, self.url)

        now = datetime.datetime.now() - datetime.timedelta(hours=8)
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            doc = DDoc(task_id=self.task_id, from_url=self.from_url, page_url=self.url, page_content=self.page_source,
                    page_level=self.now_depth, download_date=now)
            doc.save()
            self.logger.info("save URL %s" % (self.url))
        except Exception, e:
            self.logger.error('STORE ERROR\n' + str(e) + ' URL: %s \n' % self.url)
            return False
        return True


    def parse_url(self):
        res = urlparse.urlparse(self.url)
        self.netloc = res[1]
		
	
    def custom_headers(self, **kargs):

        self.headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset' : 'gb18030,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding' : 'gzip,deflate,sdch',
            'Accept-Language' : 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            #设置Host会导致TooManyRedirects, 因为hostname不会随着原url跳转而更改,可不设置
            #'Host':urlparse(self.url).hostname
            'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 \
            (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
            'Referer' : self.url,
        }
        self.headers.update(kargs)

    def is_response_avaliable(self, response):
        if response.status_code == requests.codes.ok:
            try:
                if 'html' in response.headers.get(r'content-type'):
                    return True
            except:
                pass
        return False





