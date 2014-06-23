from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from databases import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'site_SE.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.databases, name='databases'),
	url(r'^queries/(?P<db>[-\w\.]+)$', views.queries, name='queries'),
	url(r'^queries/(?P<db>[-\w\.]+)/(?P<query>[-\w\ \,\=\']+)/process/$', views.process_req, name='process_req'),
)
#urlpatterns += staticfiles_urlpatterns()
