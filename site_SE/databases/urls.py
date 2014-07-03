from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from databases import views

urlpatterns = patterns('',
    url(r'^$', views.databases, name='databases'),
	url(r'^(?P<db>[-\w\.]+)/queries/$', views.queries, name='queries'),
	url(r'^(?P<db>[-\w\.]+)/queries/(?P<query>[-\w\ \,\=\(\)\>\<\']+)/process/$', views.process_req, name='process_req'),
)
urlpatterns += staticfiles_urlpatterns()
