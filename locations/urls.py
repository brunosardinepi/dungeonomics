from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'locations'
urlpatterns = [
    path('world/<int:world_pk>/', views.location_detail, name='location_detail'),
    path('location/<int:location_pk>/', views.location_detail, name='location_detail'),

    path('world/create/', views.world_create, name='world_create'),
    path('location/create/', views.location_create, name='location_create'),
    path('world/<int:world_pk>/location/create/', views.location_create, name='location_create'),
    path('world/<int:world_pk>/location/<int:location_pk>/create/', views.location_create, name='location_create'),

    path('world/<int:world_pk>/edit/', views.world_update, name='world_update'),
    path('location/<int:location_pk>/edit/', views.location_update, name='location_update'),

    path('world/<int:world_pk>/delete/', views.world_delete, name='world_delete'),
    path('location/<int:location_pk>/delete/', views.location_delete, name='location_delete'),

    path('export/', login_required(views.WorldExport.as_view()), name='world_export'),
    path('import/', login_required(views.WorldImport.as_view()), name='world_import'),

    path('', views.location_detail, name='location_detail'),
]
