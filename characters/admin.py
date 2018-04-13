from django.contrib import admin

from . import models


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'level',)
    ordering = ('user',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'player_name', 'user',)
    ordering = ('user',)

admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Monster, CharacterAdmin)
admin.site.register(models.NPC, CharacterAdmin)
