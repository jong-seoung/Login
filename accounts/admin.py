from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "name", "is_staff")
    list_filter = ("email", "name", "nickname", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "nickname")}),
        ("Permissions", {"fields": ("is_staff",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "nickname", "is_staff"),
            },
        ),
    )
    search_fields = ("email", "name", "nickname")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
