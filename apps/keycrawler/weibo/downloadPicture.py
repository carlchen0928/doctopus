# -*- coding: utf-8 -*-

import settings
import urllib2
import string
import datetime
import time
import os
import hashlib
import logging
from bs4 import BeautifulSoup
import xml.dom.minidom as Dom

logger = logging.getLogger('my_weibo_crawler')

def filter_some(tag):
    return tag.name == 'img' and tag.has_attr('action-data') and tag.has_attr('action-type')

def getDirName(weiboId, date):
    t = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
    timestamp = int(time.mktime(t.timetuple()))

    uniq = str(weiboId) + str(timestamp)
    name = hashlib.md5(uniq).hexdigest()

    return name


def getUrlAndDownloadPicture(personTag, storePicturePath, weiboId, date):
    hasPicturesTag = personTag.find('ul', attrs={'class', 'piclist'})
    doc = Dom.Document()
    rootNode = doc.createElement('Picture')
    doc.appendChild(rootNode)

    if hasPicturesTag:
        picturesTag = hasPicturesTag.find_all(filter_some)
        if picturesTag: #如果该条微博中有图片，则建立一个文件夹存放
            dirName = getDirName(weiboId, date)
            storePicturePath += '/%s' % dirName
            if os.path.exists(storePicturePath) == False:
                os.mkdir(storePicturePath)        

        index = 1
        for pt in picturesTag:
            smallP = pt.get('src')
            logger.info(smallP)
            print smallP
    
            #largeP = string.replace(smallP, "thumbnail", "large")
            middleP = string.replace(smallP, "thumbnail", "bmiddle")
            middleP = string.replace(middleP, "square", "bmiddle")
            
            pNode = doc.createElement('img%d' % index)
            pNode.setAttribute('url', middleP)
            pNode.setAttribute('storePath', storePicturePath + '/%d.jpg' % index)
            rootNode.appendChild(pNode)
            if downloadPicture(middleP, storePicturePath, index):
                logger.info('download Picture succeed...')
                print 'download Picture succeed...'
            index += 1
            time.sleep(1)
        return doc.toprettyxml(indent='\t', newl='\n', encoding='utf-8')


def downloadPicture(url, storePicturePath, index):
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        web = opener.open(url)

        jpgData = web.read()
        fp = open(storePicturePath + '/%d.jpg' % index, 'wb')
        fp.write(jpgData)
        fp.close()
        return 1
    except Exception, e:
        logger.info(str(e) + 'Fail download %s...' % url)
        print e
        print "Fail download %s ..." % url
        return 0
    return 0



