from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from posts import views as post_views

urlpatterns = [
    url(r'^(?P<campaign_pk>\d+)/$', views.campaign_detail, name='campaign_detail'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/$', views.campaign_detail, name='campaign_detail'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/(?P<section_pk>\d+)/$', views.campaign_detail, name='campaign_detail'),

    url(r'^create/$', views.CampaignCreate.as_view(), name='campaign_create'),
    url(r'^(?P<campaign_pk>\d+)/chapter/create/$', views.chapter_create, name='chapter_create'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/create/$', views.section_create, name='section_create'),

    url(r'^(?P<campaign_pk>\d+)/edit/$', views.campaign_update, name='campaign_update'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/edit/$', views.chapter_update, name='chapter_update'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/(?P<section_pk>\d+)/edit/$', views.section_update, name='section_update'),

    url(r'^(?P<campaign_pk>\d+)/print/$', views.campaign_print, name='campaign_print'),
    url(r'^import/$', views.campaign_import, name='campaign_import'),
    url(r'^(?P<campaign_pk>\d+)/export/$', views.campaign_export, name='campaign_export'),

    url(r'^(?P<campaign_pk>\d+)/delete/$', views.campaign_delete, name='campaign_delete'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/delete/$', views.chapter_delete, name='chapter_delete'),
    url(r'^(?P<campaign_pk>\d+)/chapter/(?P<chapter_pk>\d+)/section/(?P<section_pk>\d+)/delete/$', views.section_delete, name='section_delete'),

    url(r'^(?P<campaign_pk>\d+)/party/$', login_required(views.CampaignParty.as_view()), name='campaign_party'),
    url(r'^(?P<campaign_pk>\d+)/party/invite/$', login_required(views.CampaignPartyInvite.as_view()), name='campaign_party_invite'),
    url(r'^(?P<campaign_pk>\d+)/party/remove/$', login_required(views.CampaignPartyRemove.as_view()), name='campaign_party_remove'),
    url(r'^(?P<campaign_public_url>[\w-]+)/$', login_required(views.CampaignPartyInviteAccept.as_view()), name='campaign_party_invite_accept'),
    url(r'^(?P<campaign_pk>\d+)/party/posts/create/$', login_required(post_views.PostCreate.as_view()), name='post_create'),
    url(r'^(?P<campaign_pk>\d+)/party/posts/(?P<post_pk>\d+)/delete/$', login_required(post_views.PostDelete.as_view()), name='post_delete'),

    url(r'^$', views.campaign_detail, name='campaign_detail'),
]