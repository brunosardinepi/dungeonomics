from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<item_pk>\d+)/$', views.item_detail, name='item_detail'),    
    url(r'^create/$', views.item_create, name='item_create'),
    url(r'^(?P<item_pk>\d+)/edit/$', views.item_update, name='item_update'),
    url(r'^(?P<item_pk>\d+)/delete/$', views.item_delete, name='item_delete'),
    url(r'^(?P<item_pk>\d+)/copy/$', views.item_copy, name='item_copy'),
    url(r'^$', views.item_detail, name='item_detail'),
]