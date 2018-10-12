from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views


app_name = 'votes'
urlpatterns = [
    path('<int:feature_pk>/', login_required(views.VoteView.as_view()), name='vote_view'),
]