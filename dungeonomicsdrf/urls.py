from django.contrib import admin
from django.urls import include, path
from dungeonomicsdrf import environ
from dungeonomicsdrf.views import SignupView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(f"{environ.secrets['admin']}/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', SignupView.as_view()),
    path('features/', include('features.urls')),
    path('resources/', include('resources.urls')),
]
