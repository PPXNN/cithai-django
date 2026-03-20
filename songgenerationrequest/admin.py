from django.contrib import admin
from .models import SongGenerationRequest

# Register your models here.

@admin.register(SongGenerationRequest)
class SongGenerationRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "song", "request_status", "estimated_duration", "requested_at")
    list_filter = ("request_status", "occasion", "genre", "voice_type", "mood")
    search_fields = ("title", "song__title")
    ordering = ("-requested_at",)
    readonly_fields = ("requested_at",)
    fieldsets = (
        ("Request Info", {"fields": ("song", "title", "request_status", "estimated_duration")}),
        ("Song Properties", {"fields": ("occasion", "genre", "voice_type", "mood")}),
        ("Metadata", {"fields": ("requested_at",)}),
    )