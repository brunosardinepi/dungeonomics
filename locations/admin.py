from django.contrib import admin

from . import models


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent',)
    ordering = ('name', 'parent',)
    list_filter = ('name', 'parent',)
    save_as = True

admin.site.register(models.Location, LocationAdmin)

