from django.contrib import admin

from . import models


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)
    ordering = ('user',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'player_name', 'user',)
    ordering = ('user',)

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'character',)
    order = ('name', 'character',)

admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Monster, CharacterAdmin)
admin.site.register(models.NPC, CharacterAdmin)
admin.site.register(models.GeneralCharacter, CharacterAdmin)
admin.site.register(models.Attribute, AttributeAdmin)
