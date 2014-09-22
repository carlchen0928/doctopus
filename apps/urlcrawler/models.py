from django.db import models
import pymongo
import mongoengine as mongo
from bson import ObjectId


class urlTask(models.Model):
    task_id = models.IntegerField(primary_key=True)
    task_name = models.CharField(max_length=100)
    task_filepath = models.CharField(max_length=100)
    max_depth = models.IntegerField()
    url_filter = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=100)
    class Meta:
        db_table = 'taskinfo'


class DDoc(mongo.Document):
    task_id = mongo.IntField()
    from_url = mongo.StringField(max_length=1024)
    page_url = mongo.StringField(max_length=1024)
    page_content = mongo.StringField()
    page_level = mongo.IntField()
    download_date = mongo.DateTimeField()

    meta = {
        'collection': 'doctopus', 
        'ordering': ['-download_date']
    }

class runningTask(models.Model):
    task_id = models.IntegerField()
    page_url = models.CharField(max_length=700, db_index=True)
    class Meta:
        db_table = 'taskrun'
# Create your models here.
