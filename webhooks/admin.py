from django.contrib import admin

from .models import Webhook, WebhookAttribute


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
  list_display = ('pk', 'provider',)
  ordering = list_display

@admin.register(WebhookAttribute)
class WebhookAttributeAdmin(admin.ModelAdmin):
  list_display = ('pk', 'webhook', 'key',)
  ordering = list_display
