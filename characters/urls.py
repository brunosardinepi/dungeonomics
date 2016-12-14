from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'monster/$', views.monster_detail, name='monster_detail'),
    url(r'npc/$', views.npc_detail, name='npc_detail'),
    url(r'player/$', views.player_detail, name='player_detail'),

    url(r'monster/(?P<monster_pk>\d+)/$', views.monster_detail, name='monster_detail'),
    url(r'npc/(?P<npc_pk>\d+)/$', views.npc_detail, name='npc_detail'),
    url(r'player/(?P<player_pk>\d+)/$', views.player_detail, name='player_detail'),
    
    url(r'monster/create/$', views.monster_create, name='monster_create'),
    url(r'npc/create/$', views.npc_create, name='npc_create'),
    url(r'player/create/$', views.player_create, name='player_create'),

    url(r'monster/(?P<monster_pk>\d+)/edit/$', views.monster_update, name='monster_update'),
    url(r'npc/(?P<npc_pk>\d+)/edit/$', views.npc_update, name='npc_update'),
    url(r'player/(?P<player_pk>\d+)/edit/$', views.player_update, name='player_update'),
    
    # url(r'monster/(?P<monster_pk>\d+)/delete/$', views.MonsterDelete.as_view(), name='monster_delete'),
    # url(r'npc/(?P<npc_pk>\d+)/delete/$', views.NPCDelete.as_view(), name='npc_delete'),
    url(r'monster/(?P<monster_pk>\d+)/delete/$', views.monster_delete, name='monster_delete'),
    url(r'npc/(?P<npc_pk>\d+)/delete/$', views.npc_delete, name='npc_delete'),
    url(r'player/(?P<player_pk>\d+)/delete/$', views.player_delete, name='player_delete'),
]