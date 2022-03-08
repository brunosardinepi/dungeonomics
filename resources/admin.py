from django.contrib import admin
from resources import models


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'name', 'user', 'parent')
    ordering = list_display

@admin.register(models.ResourceGroup)
class ResourceGroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name')
    ordering = list_display
