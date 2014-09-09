# -*- coding: utf-8 -*-

'''
Fetch_and_parse_and_store.py

used to fetch the page(url) and allow the user to custom header and proxies

'''
import datetime
import time
import requests
import urlparse
import tasks
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger
from apps.urlcrawler.models import DDoc

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
			response = requests.get(self.url, headers=self.headers,\
                    timeout=10, proxies=proxies)
			if self.is_response_avaliable(response):
				self.page_source = response.text
				return True
			else:
				self.logger.warning('Page not avaliable. Status code: %d URL:%s\n' \
                        % (response.status_code, self.url))
				return False
		except Exception, e:
			if retry > 0:
				return self.fetch(retry - 1)
			else:
				self.logger.debug(str(e) + ' URL: %s \n' % self.url)
				return False

	def store(self):
		#self.page_source, self.url
		now = datetime.datetime.now() - datetime.timedelta(hours=8)
		now = now.strftime('%Y-%m-%d %H:%M:%S')
		doc = DDoc(task_id=self.task_id, from_url=self.from_url, \
                page_url=self.url, page_content=self.page_source,
				 page_level=self.now_depth, download_date=now)
		doc.save() 

	# be supposed to earse the links to photo, css and js.
	def follow_links(self):

		if self.now_depth >= self.depth:
			return

		soup = BeautifulSoup(self.page_source)
		for link in soup.find_all('a', href=True):
			href = link.get('href').encode('utf8')
			if not href.startswith('http'):
				href = urlparse.urljoin(self.url, href)
				tasks.retrieve_page.delay(self.task_id, href, self.url, \
                        self.depth, self.now_depth + 1, \
                        self.allow_domains)
				time.sleep(3)
			elif href.find(self.netloc) != -1:
				tasks.retrieve_page.delay(self.task_id, href, self.url, \
                        self.depth, self.now_depth + 1, \
                        self.allow_domains)
				time.sleep(3)
			else:
				for domain in allow_domains:
					if href.find(domain) != -1:
						tasks.retrieve_page.delay(self.task_id, href, self.url,\
                                self.depth, self.now_depth + 1, \
                                self.allow_domains)


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


	


