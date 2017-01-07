from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<world_pk>\d+)/$', views.location_detail, name='location_detail'),
    url(r'^(?P<world_pk>\d+)/(?P<location_pk>\d+)/$', views.location_detail, name='location_detail'),

    url(r'^world/create/$', views.world_create, name='world_create'),
    url(r'^(?P<world_pk>\d+)/location/create/$', views.location_create, name='location_create'),

    url(r'^(?P<world_pk>\d+)/edit/$', views.world_update, name='world_update'),
    url(r'^(?P<world_pk>\d+)/(?P<location_pk>\d+)/edit/$', views.location_update, name='location_update'),

    # url(r'^import/$', views.campaign_import, name='campaign_import'),
    # url(r'^(?P<campaign_pk>\d+)/export/$', views.campaign_export, name='campaign_export'),

    url(r'^(?P<world_pk>\d+)/delete/$', views.world_delete, name='world_delete'),
    url(r'^(?P<world_pk>\d+)/(?P<location_pk>\d+)/delete/$', views.location_delete, name='location_delete'),

    url(r'^$', views.location_detail, name='location_detail'),
]