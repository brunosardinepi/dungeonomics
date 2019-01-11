from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'tavern'
urlpatterns = [
    path('campaigns/<int:pk>/',
        login_required(views.TavernCampaignDetailView.as_view()),
        name='tavern_campaign_detail'),
    path('campaigns/<int:pk>/review/',
        login_required(views.TavernCampaignReview.as_view()),
        name='tavern_campaign_review'),
    path('campaigns/<int:pk>/import/',
        login_required(views.TavernCampaignImport.as_view()),
        name='tavern_campaign_import'),

    path('characters/<int:pk>/',
        login_required(views.TavernCharacterDetailView.as_view()),
        name='tavern_character_detail'),
    path('characters/<int:pk>/review/',
        login_required(views.TavernCharacterReview.as_view()),
        name='tavern_character_review'),
    path('characters/<int:pk>/import/',
        login_required(views.TavernCharacterImport.as_view()),
        name='tavern_character_import'),

    path('items/<int:pk>/',
        login_required(views.TavernItemDetailView.as_view()),
        name='tavern_item_detail'),

    path('search/<str:type>/',
        login_required(views.TavernSearch.as_view()),
        name='tavern_search'),

    path('', login_required(views.TavernView.as_view()), name='tavern'),
]
