from django.conf.urls import patterns, url

from clustersizer import views


urlpatterns = patterns('',
	url(r'^home/$',views.home, name='home'),
	url(r'^testpage/$',views.testpage, name='testpage'),
	url(r'^testpage1/$',views.testpage1, name='testpage1'),
	url(r'^uploadfile/$',views.uploadfile, name='uploadfile'),
	url(r'^clustersizer/$',views.clustersizer, name='clustersizer'),
	url(r'^reviewclusters/$',views.reviewclusters, name='reviewclusters'),
	url(r'^clusterresults/$',views.clusterresults, name='clusterresults'),
)