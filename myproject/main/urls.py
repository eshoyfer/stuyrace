from django.conf.urls import patterns, url
from main import views
from django.conf import settings

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^profile/([1-9][0-9]*)/$', views.profile, name='profile'),
	url(r'^friends/$', views.friends, name='friends'),
	url(r'^schedule/$', views.schedule, name='schedule'),
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^results/([1-9][0-9]*)/$', views.results, name='results'),
	url(r'^event/([1-9][0-9]*)/$', views.event, name='event'),
	url(r'^profile/([1-9][0-9]*)/add/$', views.add, name='add'),
	url(r'^profile/([1-9][0-9]*)/remove/$', views.remove, name='remove'),
	url(r'^event/([1-9][0-9]*)/join/$', views.join, name='join'),
	url(r'^event/([1-9][0-9]*)/leave/$', views.leave, name='leave'),
	url(r'^create/$', views.create, name='create'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.login_user, name='login'),
	url(r'^profile/$', views.profile, name='profile_home'),
	url(r'^logout/$', views.logout_user, name='logout'),
	)
