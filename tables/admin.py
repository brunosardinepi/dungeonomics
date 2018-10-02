from django.contrib import admin

from . import models


class TableAdmin(admin.ModelAdmin):
  list_display = ('user', 'name',)
  ordering = ('user', 'name',)

class TableOptionAdmin(admin.ModelAdmin):
  list_display = ('table', 'option',)
  ordering = ('table',)

admin.site.register(models.Table, TableAdmin)
admin.site.register(models.TableOption, TableOptionAdmin)
