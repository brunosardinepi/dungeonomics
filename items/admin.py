from django.contrib import admin

from . import models


class ItemAdmin(admin.ModelAdmin):
  list_display = ('name', 'user',)
  list_filter = ('user',)

admin.site.register(models.Item, ItemAdmin)