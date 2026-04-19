from django.contrib import admin
from .models import Song

# Register your models here.
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "occasion", "genre", "voice_type", "mood", "is_private", "created_at")
    list_filter = ("occasion", "genre", "voice_type", "mood", "is_private")
    search_fields = ("title", "description", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Basic Info", {"fields": ("user", "title", "description")}),
        ("Song Properties", {"fields": ("occasion", "genre", "voice_type", "mood")}),
        ("Status", {"fields": ("audiofile_url", "is_private")}),
        ("Metadata", {"fields": ("created_at",)}),
    )