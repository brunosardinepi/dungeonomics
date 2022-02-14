from django.contrib import admin
from resources import models


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass
