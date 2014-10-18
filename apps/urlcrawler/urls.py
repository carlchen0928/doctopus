from django.conf.urls import patterns,url

urlpatterns = patterns('',
    url(r'^index', 'apps.urlcrawler.views.indexPage'),
    url(r'^myCrawls', 'apps.urlcrawler.views.myCrawls'), 
    url(r'^createCrawl', 'apps.urlcrawler.views.createCrawl'),
    url(r'^upload', 'apps.urlcrawler.views.upload'),
)
