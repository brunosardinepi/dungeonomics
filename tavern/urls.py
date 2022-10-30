from django.contrib.auth.decorators import login_required
from django.urls import path
from tavern import views


app_name = 'tavern'
urlpatterns = [
    path('campaign/<uuid:uuid>/',
        login_required(views.TavernCampaignDetailView.as_view()),
        name='tavern_campaign_detail'),
    path('campaign/<uuid:uuid>/review/',
        login_required(views.TavernCampaignReview.as_view()),
        name='tavern_campaign_review'),

    path('<str:type>/<int:pk>/',
        login_required(views.TavernCharacterDetailView.as_view()),
        name='tavern_character_detail'),
    path('<str:type>/<int:pk>/review/',
        login_required(views.TavernCharacterReview.as_view()),
        name='tavern_character_review'),
    path('<str:type>/<int:pk>/import/',
        login_required(views.TavernCharacterImport.as_view()),
        name='tavern_character_import'),

    path('search/<str:type>/',
        login_required(views.TavernSearch.as_view()),
        name='tavern_search'),

    path('', login_required(views.TavernView.as_view()), name='tavern'),
]
