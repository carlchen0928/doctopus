# -*- coding: utf-8 -*-

'''
Created on 2014-10-22
@author: Baifuyu
'''
import urllib2 
#import requests
import time
import datetime
import sys
import os
import random
import logging
import traceback

import parsePage
import weiboLogin
import myLog

class MainCrawler:

    def __init__(self, keyword, start, end):
        self.keyword = keyword
        self.start = start
        self.end = end
        self.logger = logging.getLogger('my_weibo_crawler')

    def crawl(self):

        username = r'echobfy@163.com'
        password = r'udms1234'
        cookie_file = 'weibo_login_cookies.dat'
        
        #如果cookie文件创建时间和当前时间相差超过一个小时，则重新登陆记录cookie
#        if os.path.exists('weibo_login_cookies.dat') == 1:
#            fileStatInfo = os.stat(r'weibo_login_cookies.dat')
#            fileCreatedTime = datetime.datetime.fromtimestamp(fileStatInfo.st_ctime)
#            now = datetime.datetime.now()
#            print now
#            print fileCreatedTime
#            if now - fileCreatedTime > datetime.timedelta(hours=1):
#                print 'remove weibo_login_cookies.dat succeed!'
#                os.remove(r'weibo_login_cookies.dat')

        if weiboLogin.login(username, password, cookie_file):
            print 'Login Weibo succeed!'
            self.logger.info('Login Weibo succeed!')
        else:
            print 'Login Weibo failed!'; 
            self.logger.error('Login Weibo failed!')
            return 0

        page = 1
        while True:
            url = 'http://s.weibo.com/wb/' + self.keyword + r'&xsort=time' 
            url += '&timescope=custom:' + self.start + '-0:' + self.end + '-23' + '&page=' + str(page)
            print 'go to download url: ' + url

            self.logger.info('go to download url:' + url)
            try:
                htmlDoc = urllib2.urlopen(url).read()
                ppp = parsePage.ParsePage(self.keyword, htmlDoc)
                hasNextPage = ppp.parse(page, url)
            except Exception, e:
                exc = str(traceback.print_exc())
                self.logger.error(exc)
                self.logger.error(e)
                print exc
                
            if hasNextPage == 0:
                print 'no next page'
                break
            
            time.sleep(random.randint(30, 40))
            page += 1

        return 1

    



