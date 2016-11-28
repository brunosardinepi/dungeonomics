from django.contrib import admin

from . import models


class CampaignAdmin(admin.ModelAdmin):
  list_display = ('title', 'user', 'created_at',)
  # ordering = ('-created_at',)
  list_filter = ('user',)

admin.site.register(models.Campaign, CampaignAdmin)