from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'login/$', views.LoginView.as_view(), name='login'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'signup/$', views.Signup.as_view(), name='signup'),
    url(r'delete/$', views.deactivate_user_view, name='delete'),
]