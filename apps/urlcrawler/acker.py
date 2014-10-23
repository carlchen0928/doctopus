from django.conf import settings
import redis
import base64
import binascii
import time


def setValue(task_id, url):
    basestr = base64.encodestring(url)
    acker = int(binascii.b2a_hex(basestr), 16)
    r = redis.Redis(connection_pool=settings.REDIS_POOL)
    print r.hget('task_xor', task_id)
    r.hset('task_xor', task_id, int(r.hget('task_xor', task_id)) ^ acker)

def getValue(task_id):
    r = redis.Redis(connection_pool=settings.REDIS_POOL)
    return r.hget('task_xor', task_id)
