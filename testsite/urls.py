from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^clustersizer/', include('clustersizer.urls', namespace='clustersizer')),
    urlpatterns += patterns('',
    	(r'^django-rq/', include('django_rq.urls')),
	)
)
