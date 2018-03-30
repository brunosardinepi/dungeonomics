from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from . import config
from . import views


urlpatterns = [
    url(r'^{}/'.format(config.settings['admin']), admin.site.urls),
    url(r'^accounts/password/reset/done/', views.PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    url(r'^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$', views.CustomPasswordResetFromKeyView.as_view(), name="account_reset_password_from_key"),
    url(r'^accounts/password/reset/key/done/$', views.PasswordResetFromKeyDoneView.as_view(), name="account_reset_password_from_key_done"),
    url(r'^accounts/profile/', views.profile_detail, name='profile'),
    url(r'^accounts/email/$', views.EmailView.as_view(), name='account_email'),
    url(r'^accounts/login/', views.LoginView.as_view(), name='login'),
    url(r'^accounts/signup/', views.SignupView.as_view(), name='signup'),
    url(r'^accounts/confirm-email/$', views.EmailVerificationSentView.as_view(), name='email_verification_sent'),
    url(r'^accounts/confirm-email/(?P<key>[-:\w]+)/$', views.ConfirmEmailView.as_view(), name='confirm_email'),
    url(r'^accounts/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^accounts/delete/', views.account_delete, name='account_delete'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^campaign/', include('campaign.urls', namespace='campaign')),
    url(r'^characters/', include('characters.urls', namespace='characters')),
    url(r'^donate/', views.DonateView.as_view(), name='donate'),
    url(r'^items/', include('items.urls', namespace='items')),
    url(r'^locations/', include('locations.urls', namespace='locations')),
    url(r'^privacy/', views.PrivacyView.as_view(), name='privacy'),
    url(r'^votes/', include('votes.urls', namespace='votes')),

    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    url(r'^sitemap.xml$', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
    url(r'^google35fe4699b1e0423b.html$', TemplateView.as_view(template_name="google35fe4699b1e0423b.html")),

    url(r'^$', views.home_view, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)