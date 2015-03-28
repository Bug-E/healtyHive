from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^addbee$', views.addUser, name='addbee'),
    url(r'^authorizationurl', views.getAuthorizationUrl, name='authorizationurl'),
    url(r'^isauthorized', views.isAuthorized, name='isauthorized'),
    url(r'^aggregatehealthdata', views.getAggregatedHealthData, name='aggregatehealthdata'),
    url(r'^getalldata', views.getAllData, name='getalldata'),
    url(r'^listusers', views.listUsers, name='listusers'),
)
