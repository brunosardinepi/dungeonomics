from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.wiki_home, name='home'),
    url(r'^(?P<section_pk>\d+)/$', views.wiki_home, name='home'),
    url(r'^(?P<section_pk>\d+)/chapter/(?P<subsection_pk>\d+)/$', views.wiki_home, name='home'),
]