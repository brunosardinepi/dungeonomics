from django.contrib import admin

from . import models


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'views',)
    ordering = list_display
    filter_horizontal = ('admins', 'tags',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = list_display

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Tag, TagAdmin)
