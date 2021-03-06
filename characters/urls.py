from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'characters'
urlpatterns = [
    path('monster/', views.monster_detail, name='monster_detail'),
    path('npc/', views.npc_detail, name='npc_detail'),
    path('player/', views.player_detail, name='player_detail'),

    path('monster/<int:monster_pk>/', views.monster_detail, name='monster_detail'),
    path('npc/<int:npc_pk>/', views.npc_detail, name='npc_detail'),
    path('player/<int:player_pk>/', views.player_detail, name='player_detail'),

    path('player/<int:player_pk>/campaigns/',
        login_required(views.PlayerCampaigns.as_view()),
        name='player_campaigns'),

    path('monster/create/', views.monster_create, name='monster_create'),
    path('npc/create/', views.npc_create, name='npc_create'),
    path('player/create/', views.player_create, name='player_create'),

    path('monster/<int:monster_pk>/edit/', views.monster_update, name='monster_update'),
    path('npc/<int:npc_pk>/edit/', views.npc_update, name='npc_update'),
    path('player/<int:player_pk>/edit/', views.player_update, name='player_update'),

    path('monster/<int:monster_pk>/delete/', views.monster_delete, name='monster_delete'),
    path('npc/<int:npc_pk>/delete/', views.npc_delete, name='npc_delete'),
    path('player/<int:player_pk>/delete/', views.player_delete, name='player_delete'),

    path('monster/<int:monster_pk>/copy/', views.monster_copy, name='monster_copy'),
    path('npc/<int:npc_pk>/copy/', views.npc_copy, name='npc_copy'),
    path('player/<int:player_pk>/copy/', views.player_copy, name='player_copy'),

    path('monster/export/', views.monster_export, name='monster_export'),
    path('npc/export/', views.npc_export, name='npc_export'),
    path('monster/import/', views.monster_import, name='monster_import'),
    path('npc/import/', views.npc_import, name='npc_import'),

    path('<str:type>/<int:pk>/publish/',
        login_required(views.CharacterPublish.as_view()),
        name='character_publish'),
    path('<str:type>/<int:pk>/unpublish/',
        login_required(views.CharacterUnpublish.as_view()),
        name='character_unpublish'),

    path('monster/srd/', views.monster_srd, name='monster_srd'),
    path('npc/srd/', views.npc_srd, name='npc_srd'),

    path('monsters/delete/',
        login_required(views.MonstersDelete.as_view()),
        name='monsters_delete'),
    path('npcs/delete/', login_required(views.NPCsDelete.as_view()), name='npcs_delete'),
    path('players/delete/',
        login_required(views.PlayersDelete.as_view()),
        name='players_delete'),
]
