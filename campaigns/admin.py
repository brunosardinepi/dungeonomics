from django.contrib import admin
from campaigns import models


@admin.register(models.Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    pass
