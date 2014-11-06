# -*- coding: utf-8 -*-


import mysql
import mysql.connector
import logging

import settings

logger = logging.getLogger('my_weibo_crawler')

def store(url, keyword, weiboId, userName, userUrl, date, content, picturePath):
    cnx = mysql.connector.connect(**settings.DBCONFIG)
    cursor = cnx.cursor()
    
    query = '''insert into weiboNews(url, keywords, weibo_id, user_name, user_url, date,
                content, pic_path) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % \
                (url, keyword, weiboId, userName, userUrl, date, content, picturePath)
    try:
        cursor.execute(query)
        cnx.commit()
    except Exception, e:
        logger.info(e)

    cursor.close()
    cnx.close()

    

        

