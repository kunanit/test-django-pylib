from django.conf.urls import patterns, url

from clustersizer import views


urlpatterns = patterns('',
	url(r'^upload/$',views.upload, name='upload'),
	url(r'^review/$',views.review, name='review'),
	url(r'^results/$',views.results, name='results'),
)