from django.urls import path

from . import views


app_name = 'webhooks'
urlpatterns = [
    path('<int:pk>/', views.WebhookDetail.as_view(), name='webhook_detail'),
    path('sns/', views.SNS_Webhook.as_view(), name='sns_webhook'),
    path('', views.WebhookList.as_view(), name='webhook_list'),
]
