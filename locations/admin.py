from django.contrib import admin

from . import models


class WorldAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'world',)
    ordering = ('name', 'world',)
    list_filter = ('name', 'world',)

admin.site.register(models.World, WorldAdmin)
admin.site.register(models.Location, LocationAdmin)
