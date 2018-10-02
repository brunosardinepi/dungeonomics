from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<table_pk>\d+)/$', views.table_detail, name='table_detail'),
    url(r'^create/$', views.table_create, name='table_create'),
    url(r'^(?P<table_pk>\d+)/edit/$', views.table_update, name='table_update'),
    url(r'^(?P<table_pk>\d+)/delete/$', views.table_delete, name='table_delete'),
    url(r'^$', views.table_detail, name='table_detail'),
]