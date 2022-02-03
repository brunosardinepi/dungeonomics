from django.urls import path
from campaigns import views


app_name = 'campaigns'
urlpatterns = [
    path('<int:pk>/chapters/', views.ChapterList.as_view()),
    path('<int:pk>/', views.CampaignDetail.as_view()),
    path('', views.CampaignList.as_view()),
]
