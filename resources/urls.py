from django.urls import path
from resources import views


app_name = 'resources'
urlpatterns = [
    path('<int:pk>/delete/', views.ResourceDelete.as_view()),
    path('<int:pk>/update/', views.ResourceUpdate.as_view()),
    path('<int:pk>/children/', views.ResourceChildrenList.as_view()),
    path('<int:pk>/', views.ResourceDetail.as_view(), name='resource_detail'),
    path('create/', views.ResourceCreate.as_view()),
    path('', views.ResourceList.as_view()),
]
