from django.contrib import admin

from . import models


class SectionAdmin(admin.ModelAdmin):
  list_display = ('title', 'order',)

class SubsectionAdmin(admin.ModelAdmin):
  list_display = ('title', 'order', 'section',)
  list_filter = ('section',)

admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.Subsection, SubsectionAdmin)