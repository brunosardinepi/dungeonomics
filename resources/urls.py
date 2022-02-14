from django.urls import path
from resources import views


app_name = 'resources'
urlpatterns = [
    path('<int:pk>/', views.ResourceDetail.as_view(), name='resource_detail'),
    path('', views.ResourceList.as_view()),
]
