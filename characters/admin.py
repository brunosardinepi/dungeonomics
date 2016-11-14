from django.contrib import admin

from . import models


class CharacterAdmin(admin.ModelAdmin):
  list_display = ('name', 'user', 'level')
  # ordering = ('-created_at',)
  list_filter = ('user', 'level')

admin.site.register(models.Monster, CharacterAdmin)
admin.site.register(models.NPC, CharacterAdmin)