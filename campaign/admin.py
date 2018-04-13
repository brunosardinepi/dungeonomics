from django.contrib import admin

from . import models


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at',)
    ordering = ('title', 'user', '-created_at',)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'campaign',)
    ordering = ('title', 'user', '-created_at', 'campaign',)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'campaign', 'chapter',)
    ordering = ('title', 'user', '-created_at', 'campaign', 'chapter',)

admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Chapter, ChapterAdmin)
admin.site.register(models.Section, SectionAdmin)