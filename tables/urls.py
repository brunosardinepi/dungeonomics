from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'tables'
urlpatterns = [
    path('<int:pk>/', views.table_detail, name='table_detail'),
    path('create/', views.table_create, name='table_create'),
    path('<int:pk>/edit/', views.table_update, name='table_update'),
    path('<int:pk>/delete/', views.table_delete, name='table_delete'),
    path('roll/', views.table_roll, name='table_roll'),
    path('', views.table_detail, name='table_detail'),
]
