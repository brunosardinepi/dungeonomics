from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<spell_pk>\d+)/$', views.spell_detail, name='spell_detail'),    
    url(r'^create/$', views.spell_create, name='spell_create'),
    url(r'^(?P<spell_pk>\d+)/edit/$', views.spell_update, name='spell_update'),
    url(r'^(?P<spell_pk>\d+)/delete/$', views.spell_delete, name='spell_delete'),
    url(r'^(?P<spell_pk>\d+)/copy/$', views.spell_copy, name='spell_copy'),
    url(r'^$', views.spell_detail, name='spell_detail'),
]
