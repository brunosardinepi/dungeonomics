from django.contrib import admin
from campaigns import models


@admin.register(models.Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass
