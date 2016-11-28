from django.contrib import admin

from . import models


class CampaignAdmin(admin.ModelAdmin):
  list_display = ('title', 'user', 'created_at',)
  # ordering = ('-created_at',)
  list_filter = ('user',)

class ChapterAdmin(admin.ModelAdmin):
  list_display = ('title', 'user', 'created_at', 'campaign',)
  # ordering = ('-created_at',)
  list_filter = ('user', 'campaign',)

class SectionAdmin(admin.ModelAdmin):
  list_display = ('title', 'user', 'created_at', 'campaign', 'chapter',)
  # ordering = ('-created_at',)
  list_filter = ('user', 'campaign', 'chapter',)

admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Chapter, ChapterAdmin)
admin.site.register(models.Section, SectionAdmin)