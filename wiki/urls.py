from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'wiki'
urlpatterns = [
    path('<int:pk>/', login_required(views.ArticleDetail.as_view()), name='article_detail'),
    path('create/', login_required(views.ArticleCreate.as_view()), name='article_create'),
    path('<int:pk>/edit/', login_required(views.ArticleUpdate.as_view()), name='article_update'),
    path('<int:pk>/delete/', login_required(views.ArticleDelete.as_view()), name='article_delete'),
    path('', login_required(views.ArticleDetail.as_view()), name='article_detail'),
]
