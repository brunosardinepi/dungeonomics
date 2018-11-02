from django.contrib import admin

from . import models


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'campaign', 'score',)
    ordering = list_display

admin.site.register(models.Review, ReviewAdmin)
