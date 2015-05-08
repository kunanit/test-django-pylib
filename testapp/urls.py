from django.conf.urls import patterns, url

from testapp import views


urlpatterns = patterns('',
	url(r'^home/$',views.home, name='home'),
	url(r'^testpage/$',views.testpage, name='testpage'),
)