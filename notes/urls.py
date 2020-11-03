from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'notes'
urlpatterns = [
    path('<int:pk>/edit/', views.note_update, name='note_update'),
    path('<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('<int:pk>/', views.note_detail, name='note_detail'),
    path('create/', views.note_create, name='note_create'),
    path('delete/', login_required(views.NotesDelete.as_view()), name='notes_delete'),
    path('', views.note_detail, name='note_detail'),
]
