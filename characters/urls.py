from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


app_name = 'characters'
urlpatterns = [
    url(r'^monster/$', views.monster_detail, name='monster_detail'),
    url(r'^npc/$', views.npc_detail, name='npc_detail'),
    url(r'^player/$', views.player_detail, name='player_detail'),

    url(r'^monster/(?P<monster_pk>\d+)/$', views.monster_detail, name='monster_detail'),
    url(r'^npc/(?P<npc_pk>\d+)/$', views.npc_detail, name='npc_detail'),
    url(r'^player/(?P<player_pk>\d+)/$', views.player_detail, name='player_detail'),

    url(r'^player/(?P<player_pk>\d+)/campaigns/$', login_required(views.PlayerCampaigns.as_view()), name='player_campaigns'),

    url(r'^monster/create/$', views.monster_create, name='monster_create'),
    url(r'^npc/create/$', views.npc_create, name='npc_create'),
    url(r'^player/create/$', views.player_create, name='player_create'),

    url(r'^monster/(?P<monster_pk>\d+)/edit/$', views.monster_update, name='monster_update'),
    url(r'^npc/(?P<npc_pk>\d+)/edit/$', views.npc_update, name='npc_update'),
    url(r'^player/(?P<player_pk>\d+)/edit/$', views.player_update, name='player_update'),

    url(r'^monster/(?P<monster_pk>\d+)/delete/$', views.monster_delete, name='monster_delete'),
    url(r'^npc/(?P<npc_pk>\d+)/delete/$', views.npc_delete, name='npc_delete'),
    url(r'^player/(?P<player_pk>\d+)/delete/$', views.player_delete, name='player_delete'),

    url(r'^monster/(?P<monster_pk>\d+)/copy/$', views.monster_copy, name='monster_copy'),
    url(r'^npc/(?P<npc_pk>\d+)/copy/$', views.npc_copy, name='npc_copy'),
    url(r'^player/(?P<player_pk>\d+)/copy/$', views.player_copy, name='player_copy'),

    url(r'^monster/export/$', views.monster_export, name='monster_export'),
    url(r'^npc/export/$', views.npc_export, name='npc_export'),
    url(r'^monster/import/$', views.monster_import, name='monster_import'),
    url(r'^npc/import/$', views.npc_import, name='npc_import'),

    url(r'^monster/srd/$', views.monster_srd, name='monster_srd'),
    url(r'^npc/srd/$', views.npc_srd, name='npc_srd'),

    url(r'^monsters/delete/$', views.monsters_delete, name='monsters_delete'),
    url(r'^npcs/delete/$', views.npcs_delete, name='npcs_delete'),
]
