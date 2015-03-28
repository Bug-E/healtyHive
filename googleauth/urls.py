from django.conf.urls import patterns, url

from googleauth import views

urlpatterns = patterns('',
            url(r'^googlecallback$', views.getResponse, name='googlecallback'),
            url(r'^getrequesturl$', views.getRequestUrl, name='getrequesturl'),
)
