from django.contrib import admin
from django.urls import include, path
from dungeonomicsdrf import environ


urlpatterns = [
    path(f"{environ.secrets['admin']}/", admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
]
