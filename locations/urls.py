from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^location/(?P<location_pk>\d+)/$', views.location_detail, name='location_detail'),
    url(r'^location/create/$', views.location_create, name='location_create'),
    url(r'^location/(?P<location_pk>\d+)/create/$', views.location_create, name='location_create'),
    url(r'^location/(?P<location_pk>\d+)/edit/$', views.location_update, name='location_update'),
    url(r'^location/(?P<location_pk>\d+)/delete/$', views.location_delete, name='location_delete'),
    url(r'^$', views.location_detail, name='location_detail'),
]
