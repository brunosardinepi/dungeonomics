from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/', views.wiki_home, name='wiki_home'),
]