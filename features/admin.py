from django.contrib import admin
from features import models


admin.autodiscover()
admin.site.enable_nav_sidebar = False

@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('pk', 'new')

@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'feature')
