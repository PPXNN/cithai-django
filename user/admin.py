from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email", "auth_provider", "max_song", "is_staff")
    list_filter = ("auth_provider", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    fieldsets = UserAdmin.fieldsets + (
        ("Cithai Info", {"fields": ("auth_provider", "max_song")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Cithai Info", {"fields": ("auth_provider", "max_song")}),
    )
