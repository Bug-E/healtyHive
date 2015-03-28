from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^addbee$', views.addUser, name='addbee'),
    url(r'^authorizationurl$', views.getAuthorizationUrl, name='authorizationurl'),
    url(r'^isauthorized$', views.isAuthorized, name='isauthorized'),
    url(r'^aggregatehealthdata$', views.getAggregatedHealthData, name='aggregatehealthdata'),
    url(r'^listusers$', views.listUsers, name='listusers'),
    url(r'^userdata', views.userdata, name='userdata'),
    url(r'^leaderboard$', views.leaderboard, name='leaderboard'),
    url(r'^listcoupons$', views.listCoupons, name='listcoupons'),
    url(r'^addcoupon$', views.addCoupon, name='addcoupon'),
    url(r'^addbeecoupon$', views.addBeeCoupon, name='addbeecoupon'),
)
