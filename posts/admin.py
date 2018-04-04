from django.contrib import admin

from . import models


class PostAdmin(admin.ModelAdmin):
  list_display = ('user', 'date', 'campaign', 'title',)
  list_filter = ('user',)

class CommentAdmin(admin.ModelAdmin):
  list_display = ('user', 'date', 'post',)
  list_filter = ('user',)

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)