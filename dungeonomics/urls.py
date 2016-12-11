from django.conf.urls import url, include, handler400, handler404
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^accounts/profile/', views.ProfileView.as_view(), name='profile'),
    url(r'^accounts/password/reset/done/', views.PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    url(r'^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$', views.CustomPasswordResetFromKeyView.as_view(), name="account_reset_password_from_key"),
    url(r'^accounts/password/reset/key/done/$', views.PasswordResetFromKeyDoneView.as_view(), name="account_reset_password_from_key_done"),
    url(r'^accounts/profile/', views.profile_detail, name='profile'),
    url(r'^accounts/login/', views.LoginView.as_view(), name='login'),
    url(r'^accounts/signup/', views.SignupView.as_view(), name='signup'),
    url(r'^accounts/confirm-email/$', views.EmailVerificationSentView.as_view(), name='email_verification_sent'),
    url(r'^accounts/confirm-email/(?P<key>[-:\w]+)/$', views.ConfirmEmailView.as_view(), name='confirm_email'),
    url(r'^accounts/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^accounts/delete/', views.account_delete, name='account_delete'),
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^characters/', include('characters.urls', namespace='characters')),
    url(r'^campaign/', include('campaign.urls', namespace='campaign')),
    url(r'^wiki/', include('wiki.urls', namespace='wiki')),
    url(r'^$', views.HomeView.as_view(), name='home'),
]

handler400 = 'views.error_404_view'
handler404 = 'views.error_404_view'
handler500 = 'views.error_404_view'