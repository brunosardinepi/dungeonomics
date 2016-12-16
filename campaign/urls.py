from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<campaign_pk>\d+)/$', views.campaign_detail, name='campaign_detail'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/$', views.campaign_detail, name='campaign_detail'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/(?P<section_pk>\d+)$', views.campaign_detail, name='campaign_detail'),

    url(r'^create/$', views.CampaignCreate.as_view(), name='campaign_create'),
    url(r'^(?P<campaign_pk>\d+)/chapter/create/$', views.chapter_create, name='chapter_create'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/create/$', views.section_create, name='section_create'),

    url(r'^(?P<campaign_pk>\d+)/edit/$', views.campaign_update, name='campaign_update'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/edit/$', views.chapter_update, name='chapter_update'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/(?P<section_pk>\d+)/edit/$', views.section_update, name='section_update'),

    url(r'^(?P<campaign_pk>\d+)/print/$', views.campaign_print, name='campaign_print'),
    url(r'^(?P<campaign_pk>\d+)/import/$', views.campaign_import, name='campaign_import'),

    url(r'^(?P<campaign_pk>\d+)/delete/$', views.campaign_delete, name='campaign_delete'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/delete/$', views.chapter_delete, name='chapter_delete'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/(?P<section_pk>\d+)/delete/$', views.section_delete, name='section_delete'),
    url(r'^$', views.campaign_detail, name='campaign_detail'),
]