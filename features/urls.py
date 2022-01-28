from django.urls import include, path
from features import views


app_name = 'features'
urlpatterns = [
    path('', views.FeatureList.as_view()),
]
