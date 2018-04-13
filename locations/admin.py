from django.contrib import admin

from . import models


class WorldAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)
    ordering = ('name',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'world', 'user',)
    ordering = ('name', 'world', 'user',)
    list_filter = ('world',)

admin.site.register(models.World, WorldAdmin)
admin.site.register(models.Location, LocationAdmin)
