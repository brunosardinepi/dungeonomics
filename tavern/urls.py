from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'tavern'
urlpatterns = [
    path('campaign/<int:campaign_pk>/',
        login_required(views.TavernCampaignDetailView.as_view()),
        name='tavern_campaign_detail'),
    path('campaign/<int:campaign_pk>/review/',
        login_required(views.TavernCampaignReview.as_view()),
        name='tavern_campaign_review'),
    path('campaign/<int:campaign_pk>/import/',
        login_required(views.TavernCampaignImport.as_view()),
        name='tavern_campaign_import'),

    path('<str:type>/<int:pk>/',
        login_required(views.TavernCharacterDetailView.as_view()),
        name='tavern_character_detail'),
    path('<str:type>/<int:pk>/review/',
        login_required(views.TavernCharacterReview.as_view()),
        name='tavern_character_review'),
    path('<str:type>/<int:pk>/import/',
        login_required(views.TavernCharacterImport.as_view()),
        name='tavern_character_import'),

    path('', login_required(views.TavernView.as_view()), name='tavern'),
]
