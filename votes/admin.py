from django.contrib import admin

from . import models


class VoteAdmin(admin.ModelAdmin):
  list_display = ('pk', 'user', 'date', 'feature',)
  list_filter = ('user', 'feature',)

class FeatureAdmin(admin.ModelAdmin):
  list_display = ('pk', 'new', 'description',)

admin.site.register(models.Vote, VoteAdmin)
admin.site.register(models.Feature, FeatureAdmin)