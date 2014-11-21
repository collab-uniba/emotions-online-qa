from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from databases import views

urlpatterns = patterns('',
    url(r'^$', views.databases, name='databases'),
	url(r'^(?P<db_title>[-\w\.]+)/queries/$', views.queries, name='queries'),
	url(r'^(?P<db_title>[-\w\.]+)/queries/(?P<query_id>[-\d]+)/csv/$', views.process_csv, name='process_csv'),
	url(r'^(?P<db_title>[-\w\.]+)/queries/(?P<query_id>[-\d]+)/vis/$', views.process_vis, name='process_vis'),
)
urlpatterns += staticfiles_urlpatterns()
