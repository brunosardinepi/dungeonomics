from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'monster/$', views.monster_detail, name='monster_detail'),
    url(r'npc/$', views.npc_detail, name='npc_detail'),
    url(r'monster/(?P<monster_pk>\d+)/$', views.monster_detail, name='monster_detail'),
    url(r'npc/(?P<npc_pk>\d+)/$', views.npc_detail, name='npc_detail'),
    
    url(r'monster/create/$', views.monster_create, name='monster_create'),
    url(r'npc/create/$', views.npc_create, name='npc_create'),

    # url(r'monster/(?P<monster_pk>\d+)/edit/$', views.MonsterUpdate.as_view(), name='monster_update'),
    url(r'monster/(?P<monster_pk>\d+)/edit/$', views.monster_update, name='monster_update'),
    url(r'npc/(?P<npc_pk>\d+)/edit/$', views.NPCUpdate.as_view(), name='npc_update'),
    
    url(r'monster/(?P<monster_pk>\d+)/delete/$', views.MonsterDelete.as_view(), name='monster_delete'),
    url(r'npc/(?P<npc_pk>\d+)/delete/$', views.NPCDelete.as_view(), name='npc_delete'),
]