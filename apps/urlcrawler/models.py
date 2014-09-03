from django.db import models


class urlTask(models.Model):
    task_id = models.IntegerField(primary_key=True)
    task_name = models.CharField()
    task_filepath = models.CharField(max_length=100)
    max_depth = models.IntegerField()
    url_filter = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=100)
    class Meta:
        db_table = 'taskinfo'


# Create your models here.
