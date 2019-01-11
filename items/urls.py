from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'items'
urlpatterns = [
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
    path('<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item_update'),
    path('<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('<int:pk>/copy/', views.ItemCopyView.as_view(), name='item_copy'),
    path('delete/', login_required(views.ItemsDelete.as_view()), name='items_delete'),
    path('export/', login_required(views.ItemExport.as_view()), name='item_export'),
    path('import/', login_required(views.ItemImport.as_view()), name='item_import'),
    path('', views.item_detail, name='item_detail'),
]
