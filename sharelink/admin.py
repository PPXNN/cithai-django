from django.contrib import admin
from .models import Sharelink

# Register your models here.

@admin.register(Sharelink)
class SharelinkAdmin(admin.ModelAdmin):
    list_display = ("song", "url", "is_active")
    list_filter = ("is_active",)
    search_fields = ("song__title", "url")