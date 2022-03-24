from django.contrib import admin
from app import models


admin.autodiscover()
admin.site.enable_nav_sidebar = False

@admin.register(models.PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'email', 'is_completed')
    ordering = list_display
