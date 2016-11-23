from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<campaign_pk>\d+)/$', views.campaign_detail, name='campaign_detail'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/$', views.campaign_detail, name='campaign_detail'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/(?P<section_pk>\d+)$', views.campaign_detail, name='campaign_detail'),

    url(r'^create/$', views.CampaignCreate.as_view(), name='campaign_create'),
    url(r'^(?P<campaign_pk>\d+)/chapter/create/$', views.chapter_create, name='chapter_create'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/create/$', views.section_create, name='section_create'),

    url(r'^(?P<campaign_pk>\d+)/edit/$', views.CampaignUpdate.as_view(), name='campaign_update'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/edit/$', views.ChapterUpdate.as_view(), name='chapter_update'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/(?P<section_pk>\d+)/edit/$', views.SectionUpdate.as_view(), name='section_update'),

    url(r'^(?P<campaign_pk>\d+)/delete/$', views.CampaignDelete.as_view(), name='campaign_delete'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/delete/$', views.ChapterDelete.as_view(), name='chapter_delete'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/(?P<section_pk>\d+)/delete/$', views.SectionDelete.as_view(), name='section_delete'),
]