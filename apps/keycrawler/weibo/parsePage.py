# -*- coding: utf-8 -*-

'''
Created on 2014-10-22
@author: Baifuyu
'''

from bs4 import BeautifulSoup
import logging
import sys

import storeMysql
import settings
import downloadPicture

reload(sys)
sys.setdefaultencoding('utf-8')


class ParsePage:

    def __init__(self, htmlDoc):
        assert isinstance(htmlDoc, str), 'htmlDoc is not str'
        self.htmlDoc = htmlDoc
        self.logger = logging.getLogger('root')

    def getContent(self):
        needLine = ''
        lines = self.htmlDoc.splitlines()
        for line in lines:
            if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_wb_feedlist"'):
                needLine = line
                break
        startPos = needLine.find('html":"')
        if startPos != -1:
            content = needLine[startPos + 7:
                -12].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\", "")
            return content
        return None

    def parse(self, page, url):
        self.htmlDoc = self.getContent().decode('utf-8') #获取页面JS中的内容

        if self.htmlDoc == None: return 0

        soup = BeautifulSoup(self.htmlDoc)
        # with open('tmp/html%d.log' % page, 'w') as f: 
        #   f.write(soup.prettify())

        persons = soup.find_all('dl', attrs={"class": "feed_list"})

        for person in persons:
            weiboId = person.get('mid')
            userName = person.find('a')['title']
            userUrl = person.find('a')['href']

            contentTag = person.find('p', attrs={"node-type": "feed_list_content"})
            try:
                content = contentTag.find('em', recursive=False).get_text()
            except Exception, e:
                logger.error('parse content error' + str(e))
                print str(e)
                content = ''
            try:
                #其中可能会出现原来未经转发的date,所以选择最后一个date
                date = person.find_all('a', attrs={'class': 'date'}) 
                date = date[-1]['title']
            except Exception, e:
                logger.error('parse date error' + str(e))
                print str(e)
                date = ''
            
            print userName

            storePicturePath = settings.STORE_PICTURE_PATH
            picturesXML = downloadPicture.getUrlAndDownloadPicture(person,
                    storePicturePath, weiboId, date)
            storeMysql.store(url, weiboId, userName, userUrl, date, content, picturesXML)
            
        if self.htmlDoc.find(u'下一页') != -1:  return 1
        else: return 0


if __name__ == '__main__':
    fp = open('tmp/fullPage1.log', 'r')
    htmlDoc = fp.read()

    ppp = ParsePage(htmlDoc)
    ppp.parse(1, 'www')












        
