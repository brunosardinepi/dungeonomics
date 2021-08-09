from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from posts import views as post_views


app_name = 'campaign'
urlpatterns = [
    path('<int:campaign_pk>/', views.campaign_detail, name='campaign_detail'),
    path('<int:campaign_pk>/chapter/<int:chapter_pk>/',
        views.campaign_detail, name='campaign_detail'),
    path('<int:campaign_pk>/chapter/<int:chapter_pk>/section/<int:section_pk>/',
        views.campaign_detail, name='campaign_detail'),

    path('create/', views.CampaignCreate.as_view(), name='campaign_create'),
    path('<int:campaign_pk>/chapter/create/',
        login_required(views.ChapterCreate.as_view()),
        name='chapter_create'),
    path('<int:campaign_pk>/chapter/<int:chapter_pk>/section/create/',
        login_required(views.SectionCreate.as_view()),
        name='section_create'),

    path('<int:campaign_pk>/edit/', views.CampaignUpdate.as_view(), name='campaign_update'),
    path('<int:campaign_pk>/chapter/<int:chapter_pk>/edit/',
        views.chapter_update, name='chapter_update'),
    path('<int:campaign_pk>/chapter/<int:chapter_pk>/section/<int:section_pk>/edit/',
        views.section_update, name='section_update'),

    path('<int:campaign_pk>/print/', views.campaign_print, name='campaign_print'),
    path('import/',
        login_required(views.CampaignImport.as_view()),
        name='campaign_import'),
    path('<int:campaign_pk>/export/',
        login_required(views.CampaignExport.as_view()),
        name='campaign_export'),

    path('<int:campaign_pk>/delete/', views.campaign_delete, name='campaign_delete'),
    path('<int:campaign_pk>/chapter/<int:chapter_pk>/delete/',
        views.chapter_delete, name='chapter_delete'),
    path('<int:campaign_pk>/chapter/<int:chapter_pk>/section/<int:section_pk>/delete/',
        views.section_delete, name='section_delete'),

    path('<int:campaign_pk>/party/',
        login_required(views.CampaignParty.as_view()),
        name='campaign_party'),
    path('<int:campaign_pk>/party/invite/',
        login_required(views.CampaignPartyInvite.as_view()),
        name='campaign_party_invite'),
    path('<int:campaign_pk>/party/remove/',
        login_required(views.CampaignPartyRemove.as_view()),
        name='campaign_party_remove'),
    path('<str:campaign_public_url>/',
        login_required(views.CampaignPartyInviteAccept.as_view()),
        name='campaign_party_invite_accept'),
    path('<int:campaign_pk>/party/posts/create/',
        login_required(post_views.PostCreate.as_view()),
        name='post_create'),
    path('<int:campaign_pk>/party/posts/<int:post_pk>/',
        login_required(post_views.PostDetail.as_view()),
        name='post_detail'),
    path('<int:campaign_pk>/party/posts/<int:post_pk>/delete/',
        login_required(post_views.PostDelete.as_view()),
        name='post_delete'),
    path('<int:campaign_pk>/party/players/<int:player_pk>/',
        login_required(views.CampaignPartyPlayersDetail.as_view()),
        name='campaign_party_player_detail'),

    path('<int:campaign_pk>/publish/',
        login_required(views.CampaignPublish.as_view()),
        name='campaign_publish'),
    path('<int:campaign_pk>/unpublish/',
        login_required(views.CampaignUnpublish.as_view()),
        name='campaign_unpublish'),

    path('', views.campaign_detail, name='campaign_detail'),
]
