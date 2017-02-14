from django.contrib import admin

from . import models


class WorldAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'world', 'parent_location',)
    ordering = ('name', 'world', 'parent_location',)
    list_filter = ('name', 'world', 'parent_location',)

admin.site.register(models.World, WorldAdmin)
admin.site.register(models.Location, LocationAdmin)
