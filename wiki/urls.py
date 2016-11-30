from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<section_pk>\d+)/$', views.wiki_home, name='home'),
    url(r'^(?P<section_pk>\d+)/subsection/(?P<subsection_pk>\d+)/$', views.wiki_home, name='home'),
    url(r'^$', views.wiki_home, name='home'),
]