from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from . import config
from . import views


urlpatterns = [
    path('{}/'.format(config.settings['admin']), admin.site.urls),
    path('accounts/password/reset/done/', views.PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    re_path('accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        views.CustomPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key"),
    path('accounts/password/reset/key/done/',
        views.PasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done"),
    path('accounts/profile/', views.profile_detail, name='profile'),
    path('accounts/email/', views.EmailView.as_view(), name='account_email'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/confirm-email/', views.EmailVerificationSentView.as_view(), name='email_verification_sent'),
    path('accounts/confirm-email/<str:key>/', views.ConfirmEmailView.as_view(), name='confirm_email'),
    path('accounts/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/delete/', views.account_delete, name='account_delete'),
    path('accounts/', include('allauth.urls')),
    path('tavern/', include('tavern.urls', namespace='tavern')),
    path('campaign/', include('campaign.urls', namespace='campaign')),
    path('characters/', include('characters.urls', namespace='characters')),
    path('donate/', views.DonateView.as_view(), name='donate'),
    path('items/', include('items.urls', namespace='items')),
    path('locations/', include('locations.urls', namespace='locations')),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('votes/', include('votes.urls', namespace='votes')),
    path('tables/', include('tables.urls', namespace='tables')),
    path('wiki/', include('wiki.urls', namespace='wiki')),
    path('webhooks/', include('webhooks.urls', namespace='webhooks')),

    path('error/image-size/', TemplateView.as_view(template_name="error_image_size.html")),
    path('error/image-type/', TemplateView.as_view(template_name="error_image_type.html")),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
    path('google35fe4699b1e0423b.html', TemplateView.as_view(template_name="google35fe4699b1e0423b.html")),

    path('', views.home_view, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
