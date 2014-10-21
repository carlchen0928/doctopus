from django.shortcuts import render
from apps.urlcrawler.models import *
from django.utils import simplejson
from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import datetime
from django.http import HttpResponseRedirect
import pickle
import redis

def myCrawls(request):
	#print simplejson.dumps(urlTask.objects.all().values())
	p = urlTask.objects.all()
	ret = {'item_list': [{'task_id': item.task_id, \
		'task_name': item.task_name, \
		'max_depth': item.max_depth, \
		'url_filter': item.url_filter, \
		'status': item.status, \
		'create_date': item.create_date, \
		'number': DDoc.objects(task_id=item.task_id).count()} for item in p]}
	print ret
	return render_to_response('myCrawls.html', ret)

def createCrawl(request):
	return render_to_response('createCrawl.html')


def indexPage(request):
	return render_to_response('index.html')

@csrf_exempt
def upload(request):
	if(request.method == 'POST'):
		if request.POST['upfile'] != '':
			f = handle_uploaded_file(request.FILES['urlfile'],\
				request.POST['name'])
		else:
			f = handle_uploaded_content(request.POST['content'], \
				request.POST['name'])
		url_filter = request.POST['filter'] \
			if request.POST.has_key('filter') else ''

		ptask = urlTask(task_name=request.POST['name'], \
			task_filepath=f, \
			max_depth=int(request.POST['deepth']), \
			url_filter=url_filter, \
			status="Pending", \
			create_date=datetime.datetime.now())
		ptask.save()
		#push task into QUEUEING queue
		r = redis.Redis(connection_pool=settings.REDIS_POOL)

		allow_domains = url_filter.split(',')
        info = [ptask.task_id, ptask.task_filepath, ptask.max_depth, allow_domains]
        print info
        r.lpush(settings.REDIS_QUEUEING, \
            pickle.dumps(info))
	#return render_to_response('index.html')
	return HttpResponseRedirect('/urlcrawler/index')

	#return render_to_response('index.html', context_instance=RequestContext(request))

def handle_uploaded_content(content, task_name):
	import os
	import time
	print settings.FILE_DIRS
	filepath = os.path.join(settings.FILE_DIRS, \
		task_name + '_' + str(int(time.time())))
	print filepath
	with open(filepath, 'wb+') as info:
		info.write(content)
	return filepath

def handle_uploaded_file(f, task_name):
	import os
	import time
	print settings.FILE_DIRS
	filepath = os.path.join(settings.FILE_DIRS, \
		task_name + '_' + str(int(time.time())))
	print filepath
	with open(filepath, 'wb+') as info:
		for chunk in f.chunks():
			info.write(chunk)
	return filepath
# Create your views here.
