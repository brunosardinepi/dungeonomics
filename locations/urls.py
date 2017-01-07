from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^world/(?P<world_pk>\d+)/$', views.location_detail, name='location_detail'),
    url(r'^location/(?P<location_pk>\d+)/$', views.location_detail, name='location_detail'),

    url(r'^world/create/$', views.world_create, name='world_create'),
    url(r'^location/create/$', views.location_create, name='location_create'),

    url(r'^world/(?P<world_pk>\d+)/edit/$', views.world_update, name='world_update'),
    url(r'^location/(?P<location_pk>\d+)/edit/$', views.location_update, name='location_update'),

    # url(r'^import/$', views.campaign_import, name='campaign_import'),
    # url(r'^(?P<campaign_pk>\d+)/export/$', views.campaign_export, name='campaign_export'),

    url(r'^world/(?P<world_pk>\d+)/delete/$', views.world_delete, name='world_delete'),
    url(r'^location/(?P<location_pk>\d+)/delete/$', views.location_delete, name='location_delete'),

    url(r'^$', views.location_detail, name='location_detail'),
]