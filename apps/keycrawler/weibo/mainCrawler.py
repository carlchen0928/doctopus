# -*- coding: utf-8 -*-

'''
Created on 2014-10-22
@author: Baifuyu
'''
import urllib2 
#import requests
import time
import sys
import os
import random
import logging
import traceback

import parsePage
import weiboLogin

logging.basicConfig(filename='crawler.log', level=logging.DEBUG, filemode='w')

class MainCrawler:

    def __init__(self, keyword, start, end):
        self.keyword = keyword
        self.start = start
        self.end = end

    def crawl(self):

        username = '18767105515'
        password = 'xxxxxxxxxxx'
        cookie_file = 'weibo_login_cookies.dat'
        if weiboLogin.login(username, password, cookie_file):
            print 'Login Weibo succeed!'
            logging.info('Login Weibo succeed!')
        else:
            print 'Login Weibo failed!'; 
            logging.error('Login Weibo failed!')
            return 0

        page = 1
        while True:
            url = 'http://s.weibo.com/wb/' + self.keyword + r'&xsort=time' 
            url += '&timescope=custom:' + self.start + '-0:' + self.end + '-23' + '&page=' + str(page)
            print 'go to download url: ' + url

            logging.info('go to download url:' + url)
            try:
                htmlDoc = urllib2.urlopen(url).read()
                ppp = parsePage.ParsePage(htmlDoc)
                hasNextPage = ppp.parse(page, url)
            except Exception, e:
                exc = str(traceback.print_exc())
                logging.error(exc)
                logging.error(e)
                print exc
                
            if hasNextPage == 0:
                print 'no next page'
                break
            
            time.sleep(random.randint(30, 40))
            page += 1

        return 1

    



