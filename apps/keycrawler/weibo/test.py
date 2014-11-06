# -*- coding: utf-8 -*-

import mainCrawler
import datetime

start = datetime.datetime.now() - datetime.timedelta(days=1)
start = str(start.strftime('%Y-%m-%d'))
end = start

ccc = mainCrawler.MainCrawler(u'埃博拉', start, end)
ccc.crawl()


#sss = mainCrawler.MainCrawler(u'姚明', '2014-10-22', '2014-10-22')
#sss.crawl()
