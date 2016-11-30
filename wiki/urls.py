from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<section_pk>\d+)/$', views.wiki_home, name='home'),
    url(r'^(?P<section_pk>\d+)/subsection/(?P<subsection_pk>\d+)/$', views.wiki_home, name='home'),
    url(r'^$', views.wiki_home, name='home'),

    url(r'^create/$', views.section_create, name='section_create'),
    url(r'^(?P<section_pk>\d+)/subsection/create/$', views.subsection_create, name='subsection_create'),

    url(r'^(?P<section_pk>\d+)/edit/$', views.section_update, name='section_update'),
    url(r'^(?P<section_pk>\d+)/subsection/(?P<subsection_pk>\d+)/edit/$', views.subsection_update, name='subsection_update'),

    url(r'^(?P<section_pk>\d+)/delete/$', views.section_delete, name='section_delete'),
    url(r'^(?P<section_pk>\d+)/subsection/(?P<subsection_pk>\d+)/delete/$', views.subsection_delete, name='subsection_delete'),
]