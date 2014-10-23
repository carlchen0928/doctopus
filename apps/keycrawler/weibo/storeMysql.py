# -*- coding: utf-8 -*-


import mysql
import mysql.connector
import logging

import settings

logger = logging.getLogger('root')

def store(url, weiboId, userName, userUrl, date, content, picturePath):
    cnx = mysql.connector.connect(**settings.DBCONFIG)
    cursor = cnx.cursor()
    
    query = '''insert into weiboNews(url, weibo_id, user_name, user_url, date,
                content, pic_path) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % \
                (url, weiboId, userName, userUrl, date, content, picturePath)
    try:
        cursor.execute(query)
        cnx.commit()
    except Exception, e:
        logger.info(e)

    cursor.close()
    cnx.close()

    

        

