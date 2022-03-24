from django.urls import path
from app import views


app_name = 'app'
urlpatterns = [
    path(
        'password-reset/<uuid:uuid>/',
        views.PasswordResetAction.as_view(),
        name="password_reset_action",
    ),
    path('password-reset/request/', views.PasswordResetRequest.as_view()),
]
