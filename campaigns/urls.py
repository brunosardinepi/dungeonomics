from django.urls import path
from campaigns import views


app_name = 'campaigns'
urlpatterns = [
    path('<int:pk>/delete/', views.CampaignDelete.as_view()),
    path('<int:pk>/update/', views.CampaignUpdate.as_view()),
    path('<int:pk>/', views.CampaignDetail.as_view()),
    path('create/', views.CampaignCreate.as_view()),
    path('', views.CampaignList.as_view()),
]
