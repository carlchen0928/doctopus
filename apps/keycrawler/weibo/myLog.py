import logging

logger = logging.getLogger('my_weibo_crawler')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('crawler.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - \
        %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

