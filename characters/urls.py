from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'characters'
urlpatterns = [
    path('create/', views.character_create, name='character_create'),
    path('<int:pk>/edit/', views.character_update, name='character_update'),
    path('<int:pk>/delete/',
        login_required(views.CharacterDelete.as_view()),
        name='character_delete'),
    path('<int:pk>/copy/',
        login_required(views.CharacterCopy.as_view()),
        name='character_copy'),
    path('<int:pk>/publish/',
        login_required(views.CharacterPublish.as_view()),
        name='character_publish'),
    path('<int:pk>/unpublish/',
        login_required(views.CharacterUnpublish.as_view()),
        name='character_unpublish'),
    path('delete/',
        login_required(views.CharactersDelete.as_view()),
        name='characters_delete'),

    path('player/<int:pk>/campaigns/',
        login_required(views.PlayerCampaigns.as_view()),
        name='player_campaigns'),

    path('<int:pk>/',
        login_required(views.CharacterDetail.as_view()),
        name='character_detail'),
    path('', login_required(views.CharacterDetail.as_view()), name='character_detail'),
]
